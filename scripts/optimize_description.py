#!/usr/bin/env python3
"""Optimize SKILL.md description for better trigger accuracy.

Uses Claude Agent SDK for both evaluation and improvement.

Setup:
    cd line-dev/scripts
    python3 -m venv .venv
    source .venv/bin/activate
    pip install claude-agent-sdk

Usage:
    # Via shell scripts (recommended):
    ./test_skill.sh messaging-api --max-iterations 1 --verbose
    ./test_all.sh

    # Direct:
    python optimize_description.py \
        --assessment-set ../skills/messaging-api/tests/assessment_set.json \
        --skill-path ../skills/messaging-api \
        --scope-config ../skills/messaging-api/tests/scope.json \
        --max-iterations 1 --verbose
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_scope_config(config_path: Path) -> dict:
    """Load scope-specific config (assess/improve scope lines)."""
    config = json.loads(config_path.read_text())
    return {
        "knowledge_domain": config.get("knowledge_domain", "LINE API"),
        "assess_scope": config.get("assess_scope", []),
        "improve_scope": config.get("improve_scope", []),
    }


# ---------------------------------------------------------------------------
# SKILL.md parsing
# ---------------------------------------------------------------------------

def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")
    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("SKILL.md missing closing ---")

    name, description = "", ""
    fm = lines[1:end_idx]
    i = 0
    while i < len(fm):
        line = fm[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value in (">", "|", ">-", "|-"):
                parts = []
                i += 1
                while i < len(fm) and (fm[i].startswith("  ") or fm[i].startswith("\t")):
                    parts.append(fm[i].strip())
                    i += 1
                description = " ".join(parts)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1
    return name, description, content


# ---------------------------------------------------------------------------
# Trigger assessment via Agent SDK
# ---------------------------------------------------------------------------

async def assess_single_query(
    skill_name: str,
    description: str,
    user_query: str,
    assess_scope: list[str],
) -> bool:
    """Ask Claude if it would trigger this skill for the given query."""
    scope_text = "\n".join(assess_scope)
    if scope_text:
        scope_text += "\n"

    prompt = (
        "You are simulating Claude Code's skill triggering decision.\n\n"
        "Claude Code has access to this skill:\n"
        f"  name: {skill_name}\n"
        f'  description: "{description}"\n\n'
        f"A user sends this message:\n"
        f'"{user_query}"\n\n'
        "Would Claude Code invoke this skill to help answer?\n"
        "Consider:\n"
        "- Does the query fall within the skill's described scope?\n"
        "- Is the skill's specialized knowledge needed?\n"
        f"{scope_text}\n"
        'Answer ONLY "true" or "false".'
    )

    result_text = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=[],
            max_turns=1,
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result
        elif hasattr(message, "content"):
            content = message.content
            if isinstance(content, str):
                result_text = content
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        result_text = block["text"]
                    elif hasattr(block, "text"):
                        result_text = block.text

    return "true" in result_text.strip().lower()


async def run_assessment(
    assessment_set: list[dict],
    skill_name: str,
    description: str,
    assess_scope: list[str],
    concurrency: int = 5,
    runs_per_query: int = 1,
) -> dict:
    """Run all assessment queries with bounded concurrency."""
    sem = asyncio.Semaphore(concurrency)

    async def bounded_assess(user_query: str) -> bool:
        async with sem:
            return await assess_single_query(skill_name, description, user_query, assess_scope)

    results = []
    for item in assessment_set:
        tasks = [bounded_assess(item["query"]) for _ in range(runs_per_query)]
        triggers = await asyncio.gather(*tasks)
        rate = sum(triggers) / len(triggers)
        should = item["should_trigger"]
        did_pass = (rate >= 0.5) if should else (rate < 0.5)
        results.append({
            "query": item["query"],
            "should_trigger": should,
            "trigger_rate": rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    return {
        "description": description,
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
        },
    }


# ---------------------------------------------------------------------------
# Description improvement via Agent SDK
# ---------------------------------------------------------------------------

async def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    assessment_results: dict,
    history: list[dict],
    knowledge_domain: str,
    improve_scope: list[str],
) -> str:
    """Use Claude Agent SDK to propose an improved description."""
    failed = [r for r in assessment_results["results"] if r["should_trigger"] and not r["pass"]]
    false_pos = [r for r in assessment_results["results"] if not r["should_trigger"] and not r["pass"]]

    scores = f'{assessment_results["summary"]["passed"]}/{assessment_results["summary"]["total"]}'

    prompt_parts = [
        f'You are optimizing a skill description for a Claude Code skill called "{skill_name}".',
        'A skill has a title+description that Claude sees to decide whether to invoke it.',
        'The description appears in Claude\'s "available_skills" list. Claude decides whether to invoke based solely on this.',
        "",
        f'Current description:\n"{current_description}"',
        f"\nScore: {scores}",
        "",
    ]

    if failed:
        prompt_parts.append("FAILED TO TRIGGER (should have but didn't):")
        for r in failed:
            prompt_parts.append(f'  - "{r["query"][:120]}" ({r["triggers"]}/{r["runs"]})')
        prompt_parts.append("")

    if false_pos:
        prompt_parts.append("FALSE TRIGGERS (triggered but shouldn't have):")
        for r in false_pos:
            prompt_parts.append(f'  - "{r["query"][:120]}" ({r["triggers"]}/{r["runs"]})')
        prompt_parts.append("")

    if history:
        prompt_parts.append("PREVIOUS ATTEMPTS (try something structurally different):")
        for h in history:
            prompt_parts.append(f'  [{h.get("passed", 0)}/{h.get("total", 0)}] "{h["description"][:150]}"')
        prompt_parts.append("")

    prompt_parts.extend([
        f"Skill content (first 2000 chars):\n{skill_content[:2000]}",
        "",
        "IMPORTANT CONTEXT:",
        "- Claude tends to NOT trigger skills when it thinks it already knows the answer.",
        "- LINE API changes frequently; Claude's training data is likely outdated.",
        f"- The description must make Claude feel uncertain about its {knowledge_domain} knowledge.",
        "- The description competes with other skills for Claude's attention — make it distinctive.",
    ])
    prompt_parts.extend(improve_scope)
    prompt_parts.extend([
        "- Focus on user intent, not implementation details. Use imperative voice.",
        "- Keep it 100-200 words max. Don't just add more keywords; try different approaches.",
        "",
        "Write an improved description.",
        "Respond with ONLY the description text. No quotes, no tags, no explanation.",
    ])

    prompt = "\n".join(prompt_parts)

    result_text = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=[],
            max_turns=1,
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result
        elif hasattr(message, "content"):
            content = message.content
            if isinstance(content, str):
                result_text = content
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        result_text = block["text"]
                    elif hasattr(block, "text"):
                        result_text = block.text

    new_desc = result_text.strip().strip('"').strip("'")
    if len(new_desc) > 1024:
        new_desc = new_desc[:1020] + "..."
    return new_desc if new_desc else current_description


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

async def run_loop(args):
    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md at {skill_path}", file=sys.stderr)
        sys.exit(1)

    scope_config = load_scope_config(Path(args.scope_config))
    assessment_set = json.loads(Path(args.assessment_set).read_text())
    name, original_desc, content = parse_skill_md(skill_path)
    current_desc = original_desc

    history = []
    best_desc = current_desc
    best_score = -1

    for iteration in range(1, args.max_iterations + 1):
        if args.verbose:
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"Iteration {iteration}/{args.max_iterations}", file=sys.stderr)
            print(f"Description: {current_desc[:120]}...", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)

        t0 = time.time()
        results = await run_assessment(
            assessment_set, name, current_desc,
            assess_scope=scope_config["assess_scope"],
            concurrency=args.concurrency,
            runs_per_query=args.runs_per_query,
        )
        elapsed = time.time() - t0

        summary = results["summary"]
        passed = summary["passed"]

        if args.verbose:
            pos = [r for r in results["results"] if r["should_trigger"]]
            neg = [r for r in results["results"] if not r["should_trigger"]]
            tp = sum(r["triggers"] for r in pos)
            pos_runs = sum(r["runs"] for r in pos)
            fn = pos_runs - tp
            fp = sum(r["triggers"] for r in neg)
            neg_runs = sum(r["runs"] for r in neg)
            tn = neg_runs - fp
            total_runs = tp + tn + fp + fn
            precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
            accuracy = (tp + tn) / total_runs if total_runs > 0 else 0.0
            print(
                f"Score: {passed}/{summary['total']} "
                f"precision={precision:.0%} recall={recall:.0%} "
                f"accuracy={accuracy:.0%} ({elapsed:.1f}s)",
                file=sys.stderr,
            )
            for r in results["results"]:
                status = "PASS" if r["pass"] else "FAIL"
                expect = "should" if r["should_trigger"] else "not  "
                print(
                    f"  [{status}] {expect} {r['triggers']}/{r['runs']} "
                    f"{r['query'][:60]}",
                    file=sys.stderr,
                )

        history.append({
            "iteration": iteration,
            "description": current_desc,
            "passed": passed,
            "total": summary["total"],
        })

        if passed > best_score:
            best_score = passed
            best_desc = current_desc

        if passed == summary["total"]:
            if args.verbose:
                print(f"\nAll passed at iteration {iteration}!", file=sys.stderr)
            break

        if iteration == args.max_iterations:
            break

        # Improve description
        if args.verbose:
            print("\nImproving description...", file=sys.stderr)

        current_desc = await improve_description(
            name, content, current_desc, results, history,
            knowledge_domain=scope_config["knowledge_domain"],
            improve_scope=scope_config["improve_scope"],
        )

        if args.verbose:
            print(f"New: {current_desc[:120]}...", file=sys.stderr)

    # Output
    output = {
        "original_description": original_desc,
        "best_description": best_desc,
        "final_description": current_desc,
        "iterations": len(history),
        "history": history,
    }
    json_str = json.dumps(output, indent=2, ensure_ascii=False)
    print(json_str)
    if args.output:
        Path(args.output).write_text(json_str)
    print(f"\nBest description:\n{best_desc}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Assess and optimize SKILL.md description for trigger accuracy",
    )
    parser.add_argument("--assessment-set", required=True, help="Path to assessment JSON")
    parser.add_argument("--skill-path", required=True, help="Skill directory containing SKILL.md")
    parser.add_argument("--scope-config", required=True, help="Path to scope.json")
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--runs-per-query", type=int, default=1, help="Runs per query for stability")
    parser.add_argument("--concurrency", type=int, default=5, help="Max parallel Agent SDK calls")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--output", default=None, help="Save results JSON to file")
    args = parser.parse_args()
    asyncio.run(run_loop(args))


if __name__ == "__main__":
    main()
