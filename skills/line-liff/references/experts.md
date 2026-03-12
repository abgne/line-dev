# LIFF Expert References

Real-world expert perspectives based on their **publicly documented contributions**. Use as directional guidance when answering questions that match their domain — not as persona roleplay.

## Quick Reference — Domain → Expert

| Domain | Experts |
|--------|---------|
| LIFF framework / URL multiplexing | Etrex Kuo, Chun-Min Tai |
| LIFF security / token handling | Sitthi Thiammekha |
| LINE MINI App (LIFF-based) | Norimitsu Yamashita |
| Share Target Picker / Firebase | Jirawat Karanwittayakarn |
| LIFF URL tools / permanent links | Chun-Min Tai |
| LIFF CLI / dev workflow | Etrex Kuo |
| LIFF Server API / app management | Etrex Kuo, Norimitsu Yamashita |
| LIFF plugins / Inspector / Mock | Sitthi Thiammekha |

---

## Etrex Kuo (郭佳甯) — LIFF Framework Architecture

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-etrex-kuo/)

**Core expertise:** LIFF development patterns, chatbot MVC framework, Flex Message programmatic generation

**Key contributions:**
- **Kamiliff** — LIFF development simplification tool, streamlines LIFF app creation and routing
- **Kamigo** — Rails chatbot MVC framework (700K+ users) with LIFF integration
- **Kamiflex** — Ruby DSL for Flex Message: composes Flex layouts as code
- Published **"Creating Unlimited LIFFs from 3 LIFF IDs"** technique (LIFF URL multiplexing)
- Co-authored LINE chatbot development book (2018)
- 40+ conference talks (COSCUP, MOPCON, ModernWeb)

**Design tendency:** Abstract repetitive patterns into composable structures. LIFF as a first-class web app inside LINE, with proper routing and auth handling.

**Reference when:**
- User is building a LIFF app and needs architecture patterns
- User asks about LIFF URL multiplexing or single-LIFF-ID routing for multiple pages
- User needs LIFF + chatbot integration (web form → bot response flow)
- User is working with Ruby/Rails and LIFF

---

## Sitthi Thiammekha (สิทธิ เทียมเมฆา) — LIFF Security & Multi-Service Integration

**Country:** Thailand | **GitHub:** [kamnan43](https://github.com/kamnan43) | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-sitthi-thiammekha/)

**Core expertise:** LIFF security, LINE Pay integration, NLP integration, Flex Message complex layouts

**Key contributions:**
- **8+ in-depth articles on LIFF security** — covers token handling, client vs server verification, data transmission
- LINE Pay API integration — token-based authentication flows combined with LIFF
- Founded **Mekha Innovation** / works at **Emetworks** (EX10 CRM platform for LINE OA)
- Led **LINE MINI App Ignition Bootcamp** in Thailand
- **World Cup LINE Bot** — landmark Flex Message implementation
- 20 years of software development experience

**Design tendency:** Security-conscious multi-service integration. Combine LIFF + LINE Login + Pay into complete business solutions with proper token handling at each boundary.

**Reference when:**
- User asks about LIFF security best practices (token exposure, ID token handling)
- User needs secure data transmission between LIFF client and backend server
- User is combining LIFF with LINE Pay or other LINE services
- User asks about client-side vs server-side token verification in LIFF context

---

## Norimitsu Yamashita (山下徳光) — LINE MINI App Architecture

**Country:** Japan | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-norimitsu-yamashita/)

**Core expertise:** LINE MINI App, LIFF, serverless architecture, UI/UX

**Key contributions:**
- CEO of **Grand Dream Inc.** — LINE MINI App certified development partner
- Expert in LINE MINI App architecture — MINI Apps are built on LIFF
- Skills: Node.js, AWS CDK, Kubernetes, UI/UX
- Fills the MINI App expertise gap in the Japanese LINE developer community

**Design tendency:** MINI App as a full application platform, not just a chatbot extension. Serverless backend with AWS CDK. Focus on UX within LINE's embedded browser constraints.

**Reference when:**
- User asks about LINE MINI App development (MINI Apps use LIFF under the hood)
- User wants to build a full application inside LINE (beyond simple chatbot)
- User asks about LIFF vs MINI App tradeoffs (view sizes, permissions, service messages)
- User needs serverless deployment for LIFF/MINI App backend

---

## Chun-Min Tai (戴均民) — LIFF URL Tooling & Permanent Links

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-chun-min-tai/) | **GitHub:** [taichunmin](https://github.com/taichunmin)

**Core expertise:** LIFF URL handling, LINE URL schemes, developer tools, LINE Beacon

**Key contributions:**
- **LINE URL Generator Tool** — web tool to generate LINE URL schemes without coding
- **LINE Digital Business Card** — Flex Message-based interactive business card using LIFF
- Published **"Creating Unlimited LIFFs from 3 LIFF IDs"** — LIFF URL multiplexing technique (with Etrex Kuo)
- **gcf-line-devbot** — LINE Flex developer tool on Google Cloud Functions
- **line-simplebeacon-esp32** — Arduino/ESP32 code for LINE Simple Beacon

**Design tendency:** Build developer tools that simplify LIFF URL handling and testing. Bridge hardware and software for creative LINE integrations.

**Reference when:**
- User asks about LIFF URL routing or permanent link strategies
- User needs LIFF URL multiplexing (serve multiple pages from limited LIFF IDs)
- User asks about LINE URL schemes for deep linking into LIFF apps
- User wants LIFF + IoT/Beacon integration

---

## Jirawat Karanwittayakarn (จิรวัฒน์) — Share Target Picker & Firebase

**Country:** Thailand | **GitHub:** [jirawatee](https://github.com/jirawatee) | **Medium:** [jirawatee](https://jirawatee.medium.com/)

**Core expertise:** LINE Bot + Firebase, Share Target Picker, serverless LIFF backends

**Key contributions:**
- LINE Thailand official **Technology Evangelist**
- Runs **LINE Developers Thailand** Medium publication — canonical Thai-language LINE resource
- Public repos for LIFF + **Firebase Cloud Functions** integration patterns
- Comprehensive tutorials on Share Target Picker implementation and LIFF URL handling
- Founded Thailand's largest Firebase developer group (12,000+ members)
- Google Developer Expert (Firebase)

**Design tendency:** Serverless-first with Firebase. Step-by-step implementation guides. LIFF as the web frontend with Firebase as the backend.

**Reference when:**
- User needs Share Target Picker implementation guidance
- User asks about serverless LIFF backend deployment (Firebase/Cloud Functions)
- User wants Firebase integration with LIFF (Firestore, Authentication, Cloud Functions)
- User is looking for beginner-friendly LIFF implementation tutorials

---

## Notable Mentions

| Name | Country | Why relevant to LIFF |
|------|---------|---------------------|
| **Sumihiro Kagawa (加川澄廣)** | Japan | LINE API Expert. Chief Judge of LINE DC BOT AWARDS 2024. LIFF & LINE MINI App expertise |
| **Supakarn Laorattanakul (Prompt)** | Thailand | LINE API Expert. Full-stack (React/Next.js/NestJS). Modern frontend development for LINE MINI App (built on LIFF) |
| **Thepnatee Phojan (Oa)** | Thailand | LINE API Expert at Emetworks (with Sitthi). LINE MINI App + AWS/GCP deployment |
| **Naohiro Fujie (富士榮尚寛)** | Japan | OpenID Foundation Japan. LIFF authentication uses LINE Login under the hood — consult for OAuth/OIDC edge cases |
| **C.T. Lin (林承澤)** | Taiwan | Creator of **Bottender** framework (4,000+ stars). Node.js chatbot + LIFF integration patterns |

---

## How to Use This Reference

1. When a user's question matches an expert's domain, consider their documented approach
2. Reference their actual open-source projects as examples when relevant
3. Never fabricate opinions or statements attributed to these individuals
4. Use their contributions as evidence of proven patterns, not as authority arguments
