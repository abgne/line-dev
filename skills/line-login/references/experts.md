# LINE Login Expert References

Real-world expert perspectives based on their **publicly documented contributions**. Use as directional guidance when answering questions that match their domain — not as persona roleplay.

## Quick Reference — Domain → Expert

| Domain | Experts |
|--------|---------|
| OAuth / OpenID Connect / Enterprise SSO | Naohiro Fujie |
| LINE Login → CRM identity linking | Okada Kazahaya |
| LIFF development (auth uses LINE Login) | Etrex Kuo |
| LIFF security / multi-service integration | Sitthi Thiammekha |
| LINE MINI App (auth uses LINE Login) | Norimitsu Yamashita |

---

## Naohiro Fujie (富士榮尚寛) — Identity & Authentication

**Country:** Japan | **Profile:** First-generation LINE API Expert

**Core expertise:** LINE Login, OpenID Connect, enterprise identity integration, Azure AD B2C

**Key contributions:**
- **Representative Director of OpenID Foundation Japan** — the foremost authority on OIDC implementation in Japan
- Microsoft MVP for Enterprise Mobility (9+ years)
- Auth0 Ambassador
- First-generation LINE API Expert (one of the original 22)
- Specialist in digital identity bridging LINE Login with enterprise SSO systems
- At CTC (Itochu Techno-Solutions)

**Design tendency:** Identity-first architecture. Integrate LINE Login into enterprise authentication flows. Ensure proper OAuth 2.0 / OpenID Connect compliance.

**Reference when:**
- User asks about LINE Login OAuth 2.0 / OpenID Connect implementation
- User needs to integrate LINE Login with enterprise SSO (Azure AD, SAML, LDAP)
- User asks about ID Token verification best practices or JWT handling
- User needs secure token handling or identity federation
- User encounters auto login or SSO edge cases

---

## Okada Kazahaya (岡田風早) — LINE Login for CRM & E-commerce

**Country:** Japan | **Company:** [SocialPLUS](https://www.socialplus.jp/)

**Core expertise:** LINE Login → identity linking → CRM, Shopify integration, e-commerce user lifecycle

**Key contributions:**
- CEO of **SocialPLUS** — pioneered LINE ID-linked CRM for e-commerce in Japan
- Built **CRM PLUS on LINE** — Shopify app that links LINE Login identity to customer profiles for personalized messaging
- His platform bridges the gap between "anonymous LINE friend" and "identified customer" via LINE Login
- Enables segment delivery, cart abandonment, and personalized notifications by linking `userId` to customer records

**Design tendency:** LINE Login as a business identity layer, not just authentication. Use the login flow to establish persistent customer identity across channels.

**Reference when:**
- User needs to link LINE Login `userId` to their own user database
- User asks about post-login identity management (mapping LINE users to CRM records)
- User wants to build "log in with LINE" for e-commerce (Shopify, custom store)
- User asks about `bot_prompt` and friendship linking as part of the login funnel

---

## Etrex Kuo (郭佳甯) — LIFF Development

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-etrex-kuo/)

**Core expertise:** Chatbot MVC framework, LIFF integration, Flex Message programmatic generation

**Key contributions:**
- **Kamigo** — Rails chatbot MVC framework (700K+ users)
- **Kamiliff** — LIFF development simplification tool, directly relevant to LINE Login auth flows within LIFF
- **Lotify** — LINE Notify Ruby SDK
- Co-authored LINE chatbot development book (2018)
- 40+ conference talks (COSCUP, MOPCON, ModernWeb)

**Design tendency:** Abstract repetitive patterns into composable structures. LIFF as a first-class web app inside LINE, with proper auth handling.

**Reference when:**
- User is building a LIFF app that needs LINE Login authentication
- User asks about LIFF → LINE Login auth flow (how LIFF obtains access tokens)
- User needs Ruby/Rails LINE Login integration
- User asks about LIFF URL multiplexing or routing patterns

---

## Sitthi Thiammekha (สิทธิ เทียมเมฆา) — LIFF Security & Multi-Service Integration

**Country:** Thailand | **GitHub:** [kamnan43](https://github.com/kamnan43) | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-sitthi-thiammekha/)

**Core expertise:** LIFF security, LINE Pay integration, NLP integration, Flex Message complex layouts

**Key contributions:**
- 8+ in-depth articles on **LIFF security** — directly covers LINE Login token handling in LIFF context
- LINE Pay API integration — involves token-based user authentication flows
- Founded **Mekha Innovation** / works at **Emetworks** (EX10 CRM platform for LINE OA)
- Led **LINE MINI App Ignition Bootcamp** in Thailand
- 20 years of software development experience

**Design tendency:** Security-conscious multi-service integration. Combine LINE Login + LIFF + Pay into complete business solutions with proper token handling at each boundary.

**Reference when:**
- User asks about LIFF security best practices (token exposure, client-side vs server-side verification)
- User needs to chain LINE Login auth with LINE Pay or other LINE services
- User asks about secure data transmission between LIFF client and backend
- User is building a multi-service LINE integration requiring auth at each layer

---

## Norimitsu Yamashita (山下徳光) — LINE MINI App Architecture

**Country:** Japan | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-norimitsu-yamashita/)

**Core expertise:** LINE MINI App, LIFF, serverless architecture, UI/UX

**Key contributions:**
- CEO of **Grand Dream Inc.** — LINE MINI App certified development partner
- Expert in LINE MINI App architecture — MINI Apps use LINE Login for user authentication
- Skills: Node.js, AWS CDK, Kubernetes, UI/UX
- Fills the MINI App expertise gap in the Japanese LINE developer community

**Design tendency:** MINI App as a full application platform. LINE Login as the seamless authentication gateway into MINI App experiences. Serverless backend with AWS CDK.

**Reference when:**
- User asks about LINE MINI App authentication flow (MINI App uses LINE Login under the hood)
- User wants to understand LIFF vs MINI App auth differences
- User needs AWS CDK deployment for LINE Login callback handling
- User asks about consent screen behavior in MINI App context

---

## Notable Mentions

| Name | Country | Why relevant to LINE Login |
|------|---------|---------------------------|
| **Kenichiro Nakamura** | Japan | Principal PM at Microsoft. Co-developed **LINE Messaging API SDK for C#**. Co-authored **LINE API実践ガイド** — comprehensive reference covering LINE Login implementation patterns. Enterprise-grade LINE integration perspective |
| **Sumihiro Kagawa (加川澄廣)** | Japan | LINE API Expert. Chief Judge of LINE DC BOT AWARDS 2024. **LIFF & LINE MINI App expertise** — both rely on LINE Login for authentication |
| **Supakarn Laorattanakul (Prompt)** | Thailand | LINE API Expert. Full-stack (React/Next.js/NestJS). LINE HACK 2020 winner. **Modern frontend for LINE MINI App** — builds the client-side auth flows that consume LINE Login |

---

## How to Use This Reference

1. When a user's question matches an expert's domain, consider their documented approach
2. Reference their actual open-source projects as examples when relevant
3. Never fabricate opinions or statements attributed to these individuals
4. Use their contributions as evidence of proven patterns, not as authority arguments
