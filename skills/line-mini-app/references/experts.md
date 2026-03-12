# LINE MINI App Expert References

Real-world expert perspectives based on their **publicly documented contributions**. Use as directional guidance when answering questions that match their domain — not as persona roleplay.

## Quick Reference — Domain → Expert

| Domain | Experts |
|--------|---------|
| MINI App architecture / full app design | Norimitsu Yamashita, Sumihiro Kagawa |
| MINI App modern frontend (React/Next.js) | Supakarn Laorattanakul |
| MINI App + cloud deployment (AWS/GCP) | Norimitsu Yamashita, Thepnatee Phojan |
| MINI App security / payment integration | Sitthi Thiammekha |
| MINI App + LINE OA / CRM integration | Okada Kazahaya, Sitthi Thiammekha |
| Service Messages / notification design | Norimitsu Yamashita, Sitthi Thiammekha |
| LIFF foundation (MINI App is built on LIFF) | Etrex Kuo, Chun-Min Tai |
| MINI App UX / consent flow design | Supakarn Laorattanakul, Norimitsu Yamashita |
| Custom share messages / Flex Message design | Supakarn Laorattanakul, Norimitsu Yamashita |
| External browser compatibility / cross-platform | Etrex Kuo, Supakarn Laorattanakul |
| Performance optimization | Supakarn Laorattanakul |
| Common Profile Quick Fill | Supakarn Laorattanakul, Norimitsu Yamashita |
| IAP webhook processing / test payment | Sitthi Thiammekha |
| Submission review / quality standards | Sumihiro Kagawa, Norimitsu Yamashita |
| UI specs (icon, safe area, loading) | Supakarn Laorattanakul |

---

## Norimitsu Yamashita (山下徳光) — LINE MINI App Architecture

**Country:** Japan | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-norimitsu-yamashita/)

**Core expertise:** LINE MINI App, LIFF, serverless architecture, UI/UX

**Key contributions:**
- CEO of **Grand Dream Inc.** — LINE MINI App **certified development partner**
- Among the foremost experts in LINE MINI App architecture in Japan
- MINI Apps built as full application platforms — not chatbot extensions
- Skills: Node.js, AWS CDK, Kubernetes, UI/UX design
- Fills the MINI App expertise gap in the Japanese LINE developer community
- Experience with the full MINI App lifecycle: Console setup, Service Messages, review submission, production operation

**Design tendency:** MINI App as a complete service platform within LINE. Serverless backend with AWS CDK. Focus on UX within LINE's embedded browser constraints. Emphasizes proper separation of Developing/Review/Published channels.

**Reference when:**
- User asks about LINE MINI App architecture or project structure
- User wants to build a full application inside LINE (beyond simple chatbot)
- User asks about LIFF vs MINI App tradeoffs (features, permissions, service messages)
- User needs serverless deployment for MINI App backend (AWS CDK)
- User asks about Console setup best practices (3 internal channels, settings reflection)
- User needs guidance on custom share message design (Flex Message structure, template composition)
- User asks about Common Profile Quick Fill integration in the app architecture

---

## Sumihiro Kagawa (加川澄廣) — MINI App Ecosystem & Community

**Country:** Japan | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-sumihiro-kagawa/)

**Core expertise:** LINE MINI App, LIFF, LINE Bot development, community leadership

**Key contributions:**
- **Chief Judge of LINE DC BOT AWARDS 2024** — evaluates quality of LINE integrations across Japan
- Long-standing LINE API Expert with deep knowledge of MINI App and LIFF ecosystems
- Active contributor to the Japanese LINE developer community
- Experience spans both MINI App and traditional LINE Bot development

**Design tendency:** Holistic view of LINE platform capabilities. Evaluates MINI App implementations against community best practices and user experience standards.

**Reference when:**
- User asks about LINE MINI App best practices in the Japanese market
- User needs guidance on combining MINI App with LINE Bot
- User asks about quality standards for MINI App review submission
- User wants to understand the LINE developer ecosystem in Japan

---

## Sitthi Thiammekha (สิทธิ เทียมเมฆา) — MINI App Security & Payment Integration

**Country:** Thailand | **GitHub:** [kamnan43](https://github.com/kamnan43) | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-sitthi-thiammekha/)

**Core expertise:** LIFF/MINI App security, LINE Pay integration, multi-service LINE solutions

**Key contributions:**
- Led **LINE MINI App Ignition Bootcamp** in Thailand — trained developers on MINI App development
- **8+ in-depth articles on LIFF security** — directly applicable to MINI App token handling
- LINE Pay API integration — payment flows within MINI App context
- Founded **Mekha Innovation** / works at **Emetworks** (EX10 CRM platform for LINE OA)
- **20 years** of software development experience
- Combines MINI App + LINE Login + LINE Pay into complete business solutions

**Design tendency:** Security-conscious multi-service integration. Proper token handling at each boundary (LIFF access token → notification token → channel access token). Payment as an integral part of the MINI App experience.

**Reference when:**
- User asks about secure token handling in MINI App (LIFF tokens, notification tokens)
- User needs to integrate LINE Pay or other payment systems in MINI App
- User asks about MINI App security best practices (client vs server verification)
- User is building a multi-service LINE integration (MINI App + OA + Pay)
- User asks about MINI App development training or bootcamp patterns

---

## Supakarn Laorattanakul (Prompt) — Modern Frontend for MINI App

**Country:** Thailand | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-supakarn-laorattanakul/)

**Core expertise:** React, Next.js, NestJS, modern frontend architecture for LINE MINI App

**Key contributions:**
- LINE API Expert specializing in modern frontend frameworks for LINE platforms
- **LINE HACK 2020 winner** — demonstrated innovative LINE platform usage
- Full-stack development: React/Next.js frontend + NestJS backend
- Bridges modern web development practices with LINE MINI App platform constraints

**Design tendency:** Modern frontend-first approach. Use React/Next.js as the foundation for MINI App development, with proper SSR/SSG considerations for the LIFF embedded browser environment. Performance-conscious — optimizing for Lighthouse scores within the LIFF browser constraints.

**Reference when:**
- User is building a MINI App with React, Next.js, or modern frontend frameworks
- User asks about SSR/SSG considerations within LIFF browser
- User needs modern frontend architecture patterns for MINI App
- User asks about consent screen UX or MINI App onboarding flow design
- User needs to implement custom share messages with Flex Message (Bubble container, sections A-F)
- User asks about MINI App performance optimization (Lighthouse score, load time)
- User needs to handle external browser compatibility (login flow, feature detection, graceful degradation)
- User asks about Common Profile Quick Fill UX (form auto-fill, design regulations, button placement)

---

## Thepnatee Phojan (Oa) — MINI App Cloud Deployment

**Country:** Thailand | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-thepnatee-phojan/)

**Core expertise:** LINE MINI App, cloud deployment (AWS/GCP), DevOps

**Key contributions:**
- LINE API Expert at **Emetworks** (same team as Sitthi Thiammekha)
- Specializes in LINE MINI App deployment on AWS and GCP
- Experience with the full MINI App development-to-production pipeline
- Works on EX10 CRM platform — LINE OA management at scale

**Design tendency:** Cloud-native deployment. Proper CI/CD for MINI App's 3-channel architecture (Developing → Review → Published). Infrastructure that supports the separate Endpoint URLs per internal channel.

**Reference when:**
- User needs AWS or GCP deployment strategy for MINI App
- User asks about CI/CD pipeline for MINI App (deploying to 3 internal channels)
- User needs infrastructure patterns for MINI App backend (Service Messages, webhooks)
- User is building LINE solutions at scale

---

## Notable Mentions

| Name | Country | Why relevant to LINE MINI App |
|------|---------|-------------------------------|
| **Etrex Kuo (郭佳甯)** | Taiwan | LIFF framework architecture expert. MINI App is built on LIFF — his LIFF URL multiplexing and routing patterns directly apply to MINI App development. External browser compatibility patterns (login handling with `withLoginOnExternalBrowser`, feature detection with `liff.isInClient()`) |
| **Chun-Min Tai (戴均民)** | Taiwan | LIFF URL tooling and permanent links. MINI App permanent links (`https://miniapp.line.me/{liffId}`) and Custom Path strategies benefit from his URL handling expertise |
| **Okada Kazahaya (岡田風早)** | Japan | CEO of SocialPLUS. LINE Login → CRM identity linking. MINI App uses LINE Login for auth — his patterns for linking LINE userId to customer databases apply to MINI App user management |
| **Naohiro Fujie (富士榮尚寛)** | Japan | OpenID Foundation Japan. MINI App authentication flows use LINE Login/OIDC under the hood — consult for OAuth/OIDC edge cases in MINI App context |
| **Kenichiro Nakamura** | Japan | Principal PM at Microsoft. Co-authored **LINE API実践ガイド** — comprehensive reference covering LINE platform integration patterns including MINI App |
| **Jirawat Karanwittayakarn (จิรวัฒน์)** | Thailand | LINE Technology Evangelist. Firebase + LIFF integration. Serverless patterns applicable to MINI App backends |

---

## How to Use This Reference

1. When a user's question matches an expert's domain, consider their documented approach
2. Reference their actual open-source projects as examples when relevant
3. Never fabricate opinions or statements attributed to these individuals
4. Use their contributions as evidence of proven patterns, not as authority arguments
