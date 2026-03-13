# line-dev

AI agent skills for LINE platform development. Build bots, login flows, LIFF apps, MINI Apps, notification messages, and LINE stickers/emoji/themes with up-to-date API references.

## Contents

- [Install as Claude Code Plugin](#claude-code-plugin)
- [Install as Skills](#install-as-skills)
- [Available Skills](#available-skills)
- [Testing](#testing-trigger-accuracy)

---

## Claude Code Plugin

Install all skills as a Claude Code plugin:

```bash
/plugin marketplace add abgne/line-dev
/plugin install line-dev@abgne-line-dev
```

Or test locally without installing:

```bash
claude --plugin-dir /path/to/line-dev
```

After install, reload with `/reload-plugins`.

---

## Install as Skills

### All Skills

```bash
npx skills add abgne/line-dev
```

### Specific Skills

```bash
npx skills add abgne/line-dev@messaging-api
npx skills add abgne/line-dev@line-login
npx skills add abgne/line-dev@line-liff
npx skills add abgne/line-dev@line-mini-app
npx skills add abgne/line-dev@line-notification-message
npx skills add abgne/line-dev@line-creators-market
```

---

## Available Skills

| Skill | Description |
|-------|-------------|
| [messaging-api](skills/messaging-api/) | Webhook, push/reply/multicast, Flex Message, Rich Menu, narrowcast, audience, insights, coupons, channel tokens |
| [line-login](skills/line-login/) | OAuth 2.0, PKCE, ID Token JWT verification, token management, bot linking, login button design |
| [line-liff](skills/line-liff/) | LIFF SDK, liff.init, sendMessages, Share Target Picker, QR scan, permanent links, pluggable SDK |
| [line-mini-app](skills/line-mini-app/) | Service Messages, Common Profile Quick Fill, In-App Purchase, Console setup, submission review |
| [line-notification-message](skills/line-notification-message/) | Phone-number-based PNP push, SHA256 hashing, template/flexible types, delivery webhook, consent flow, SMS auth |
| [line-creators-market](skills/line-creators-market/) | Sticker creation (7 types), emoji, themes, technical specs, review guidelines, revenue model, AI usage declaration, LINE Sticker Maker, market strategy |

Each skill includes reference files covering API specs, expert guidance, and region-specific details for **Japan**, **Thailand**, and **Taiwan**.

Skills load progressively — metadata is always in context, SKILL.md body loads on trigger, reference files load as needed.

---

## Testing Trigger Accuracy

Each skill has an assessment set (should-trigger + should-not-trigger queries in 4 languages: en, ja, zh-TW, th) to measure description quality.

### Setup

```bash
cd scripts
python3 -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk
```

### Run

```bash
# Test one skill
./test_skill.sh messaging-api --max-iterations 1 --verbose

# Test all skills
./test_all.sh --verbose

# Auto-optimize description (iterate up to 3 times)
./test_skill.sh line-login --max-iterations 3 --verbose --output results.json
```

### Current Scores

| Skill | Accuracy | Queries |
|-------|----------|---------|
| messaging-api | 100% | 70/70 |
| line-notification-message | 100% | 70/70 |
| line-mini-app | 99% | 174/176 |
| line-login | 92% | 60/65 |
| line-liff | 92% | 66/72 |
| line-creators-market | 100% | 68/68 |
