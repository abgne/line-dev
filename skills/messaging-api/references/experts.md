# Expert Contributions Reference

Real-world expert perspectives based on their **publicly documented contributions**. Use as directional guidance when answering questions that match their domain — not as persona roleplay.

## Quick Reference — Domain → Expert

| Domain | Experts |
|--------|---------|
| Framework/architecture | Etrex Kuo, C.T. Lin |
| SDK/Go/OpenAPI | Evan Lin, Tokuhiro Matsuno |
| Flex Message design | Sitthi, Etrex, Chun-Min Tai |
| Rich Menu | Jirawat |
| Group chat | Evan Lin, NiJia Lin |
| AI/NLP integration | Dr. Winn, Evan Lin |
| Audience/Narrowcast | Noda Daisuke |
| Insights/analytics | Jin Hsueh |
| Coupon/campaigns | Tsutsumi Takehiro |
| URL schemes/deep linking | Chun-Min Tai, Jirawat |
| Chatbot UX design | MingHui-D. Wen |
| Beginner/prototype | Sugawara, Jirawat |
| Python SDK | NiJia Lin |
| Enterprise e-commerce | Punsiri Boonyakiat |

---

## Etrex Kuo (郭佳甯) — Framework Architecture

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-etrex-kuo/)

**Core expertise:** Chatbot MVC architecture, Flex Message programmatic generation, LIFF

**Key contributions:**
- **Kamigo** — Rails chatbot MVC framework: share controllers/models between web and chatbot, only write separate views. 700K+ users
- **Kamiflex** — Ruby DSL for Flex Message: eliminates hand-writing JSON, composes Flex layouts as code
- **Kamiliff** — LIFF development simplification tool
- **Lotify** — LINE Notify Ruby SDK
- Co-authored LINE chatbot development book (2018)
- 40+ conference talks (COSCUP, MOPCON, ModernWeb)

**Design tendency:** Abstract repetitive patterns into composable, reusable structures. Treat chatbot as a first-class application with proper MVC separation.

**Reference when:**
- User needs to design programmatic Flex Message generation (not hand-crafted JSON)
- User is building a chatbot with complex conversation flows that need MVC structure
- User asks about LIFF integration patterns
- User is working with Ruby/Rails

---

## Evan Lin (林敬堯) — SDK Architecture & DevRel

**Country:** Taiwan | **GitHub:** [kkdai](https://github.com/kkdai) | **Blog:** [evanlin.com](https://www.evanlin.com/)

**Core expertise:** LINE Bot SDK (Go), OpenAPI SDK generation, AI + LINE Bot integration

**Key contributions:**
- Core contributor to **line-bot-sdk-go**: message quota, broadcast, webhook testing
- Led SDK migration from hand-written to **OpenAPI/Swagger generated** code (v8)
- LINE Bot + GCP Speech-to-Text + Flex Message integration
- AI Agent LINE Bot using Google ADK
- LINE Taiwan DevRel team lead, Google Developer Expert (Go & AI)

**Design tendency:** Type-safe SDK design. Leverage OpenAPI specs for SDK generation rather than manual implementation. Bridge AI services with LINE Bot.

**Reference when:**
- User asks about SDK choice or architecture decisions
- User needs Go-based LINE Bot implementation
- User wants to integrate AI/ML services (speech, vision, LLM) with LINE Bot
- User asks about OpenAPI spec-based development
- User needs group chat bot implementation (has `linebot-group` demo repo and group chat summary generator)

---

## C.T. Lin (林承澤) — Node.js Chatbot Framework

**Country:** Taiwan | **GitHub:** [chentsulin](https://github.com/chentsulin)

**Core expertise:** Node.js chatbot framework design, Flex Message encapsulation, multi-platform chatbot architecture

**Key contributions:**
- **Bottender** — Node.js chatbot framework (4,000+ GitHub stars), built at Yoctol; supports LINE, Messenger, Telegram, Slack
- Created **bottender-kamigo-example** — reimplemented Kamigo's chatbot logic in Bottender, bridging two major Taiwan-born frameworks
- Presented on Flex Message encapsulation patterns at Chatbots Meetup
- Architect at Dcard

**Design tendency:** Platform-agnostic chatbot architecture. Build once, deploy to multiple messaging platforms. Encapsulate Flex Message complexity behind clean APIs.

**Reference when:**
- User needs a multi-platform chatbot (not LINE-only)
- User wants Node.js/TypeScript chatbot framework
- User asks about abstracting Flex Message generation in JavaScript
- User is comparing chatbot framework options

---

## MingHui-D. Wen (溫明輝) — Chatbot UX & Conversation Design

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-minghui-d-wen/)

**Core expertise:** Conversational UI design, HCI research, chatbot product-market fit

**Key contributions:**
- Professor & Director of Innovation Incubation Center at National Taipei University of Business
- Co-founder of **Quants (微股力)** — stock investment chatbot, 300-400K LINE users
- Co-founder of **CheckChick (記帳雞)** — expense tracker chatbot, 300-400K LINE users
- **5 patents** on conversational UI
- 30+ invited talks on chatbot UX design
- LINE TECHPULSE 2017 speaker

**Design tendency:** Research-driven conversation design. Validate chatbot UX with real user data. Balance utility and engagement in conversational interfaces.

**Reference when:**
- User asks about chatbot conversation flow design (not just API integration)
- User needs to design user-friendly chatbot interactions
- User is building a finance or utility chatbot
- User asks "how should my bot respond" rather than "how do I send a message"

---

## Chun-Min Tai (戴均民) — LINE Beacon & Flex Tooling

**Country:** Taiwan | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/tw-chun-min-tai/) | **GitHub:** [taichunmin](https://github.com/taichunmin)

**Core expertise:** LINE Beacon hardware, Flex Message developer tools, DevOps for chatbot

**Key contributions:**
- **LINE URL Generator Tool** — web tool to generate LINE URL schemes without coding
- **LINE Digital Business Card** — Flex Message-based interactive business card tool using LIFF
- **gcf-line-devbot** — LINE Flex developer tool on Google Cloud Functions
- **line-simplebeacon-esp32** — Arduino/ESP32 code for LINE Simple Beacon hardware
- Published "Creating Unlimited LIFFs from 3 LIFF IDs" — LIFF URL multiplexing technique
- Developer of **YouBike Today** chatbot
- Presented LINE Beacon deployment at COSCUP 2023, Docker-based chatbot dev at COSCUP 2019

**Design tendency:** Bridge hardware and software. Use ESP32/Arduino for physical LINE Beacon triggers. Build developer tools that simplify Flex Message creation and testing.

**Reference when:**
- User asks about LINE Beacon implementation or hardware setup
- User needs Flex Message development/testing tools
- User asks about LINE URL schemes or deep linking (has URL Generator tool)
- User needs LIFF URL routing or multiplexing techniques
- User wants to integrate IoT devices with LINE Bot
- User asks about Docker-based chatbot development workflow

---

## NiJia Lin (louis70109) — Python SDK & Community

**Country:** Taiwan | **GitHub:** [louis70109](https://github.com/louis70109) | **Blog:** [nijialin.com](https://nijialin.com/)

**Core expertise:** LINE Bot Python SDK, LINE Notify, developer community organization

**Key contributions:**
- LINE Taiwan **Technology Evangelist**
- Contributor to **line-bot-sdk-python**
- Creator of **lotify** — LINE Notify API wrapper (Python)
- Created **line-bot-group-event-bot** — handles group events: unsend, join, leave, memberJoined, memberLeft
- Created **Announcer** — tool to announce messages to LINE Users/Groups/Rooms
- Co-organizer of **Chatbot Developers Taiwan** meetup community
- Regular speaker at COSCUP, Chatbots Meetup

**Design tendency:** Python-first implementation. Community-driven development. Make LINE APIs accessible through clear documentation and community events.

**Reference when:**
- User wants Python-based LINE Bot implementation
- User asks about LINE Notify integration
- User needs LINE Bot SDK Python usage patterns
- User needs group chat event handling (join/leave/memberJoined/memberLeft)
- User is looking for community resources in Taiwan

---

## Nobisuke Sugawara (菅原のびすけ) — Education & Rapid Prototyping

**Country:** Japan | **GitHub:** [n0bisuke](https://github.com/n0bisuke) | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-nobisuke-sugawara/)

**Core expertise:** Node.js LINE Bot, IoT + chatbot integration, developer education

**Key contributions:**
- **First-generation LINE API Expert** (one of the original 22 worldwide)
- Created the canonical "Making LINE Bot within an hour" Node.js workshop
- Founded **IoTLT** — Japan's largest IoT developer community (5,000+ members)
- Core organizer of **LINE BOT AWARDS**
- Founded dotstudio Inc., adjunct lecturer at Digital Hollywood University
- Co-author of **LINE API 実践ガイド** (Mynavi, 2020)

**Design tendency:** Minimize time-to-working-bot. Node.js-first. Combine physical (IoT/hardware) with chatbot for creative prototypes.

**Reference when:**
- User is a beginner asking "how do I get started with LINE Bot?"
- User needs a quick prototype or proof-of-concept
- User wants Node.js implementation
- User asks about IoT + LINE Bot integration (beacon, hardware triggers)

---

## Naohiro Fujie (富士榮尚寛) — Identity & Authentication

**Country:** Japan | **Profile:** First-generation LINE API Expert

**Core expertise:** LINE Login, OpenID Connect, enterprise identity integration, Azure AD B2C

**Key contributions:**
- **Representative Director of OpenID Foundation Japan**
- Microsoft MVP for Enterprise Mobility (9+ years)
- Auth0 Ambassador
- First-generation LINE API Expert (one of the original 22)
- Specialist in digital identity bridging LINE Login with enterprise SSO systems
- At CTC (Itochu Techno-Solutions)

**Design tendency:** Identity-first architecture. Integrate LINE Login into enterprise authentication flows. Ensure proper OAuth 2.0 / OpenID Connect compliance.

**Reference when:**
- User asks about LINE Login implementation or best practices
- User needs to integrate LINE Login with existing enterprise SSO (Azure AD, SAML, etc.)
- User asks about OAuth 2.0 / OpenID Connect in LINE context
- User needs secure token handling or identity federation

---

## Norimitsu Yamashita (山下徳光) — LINE MINI App Architecture

**Country:** Japan | **Profile:** [LINE API Expert](https://developers.line.biz/ja/community/api-experts/jp-norimitsu-yamashita/)

**Core expertise:** LINE MINI App, LIFF, serverless architecture, UI/UX

**Key contributions:**
- CEO of **Grand Dream Inc.** — LINE MINI App certified development partner
- Expert in LINE MINI App architecture and LIFF integration
- Skills: Node.js, AWS CDK, Kubernetes, UI/UX
- Fills the MINI App expertise gap in the Japanese LINE developer community

**Design tendency:** MINI App as a full application platform, not just a chatbot extension. Serverless backend with AWS CDK. Focus on UX within LINE's embedded browser constraints.

**Reference when:**
- User asks about LINE MINI App development or architecture
- User wants to build a full application inside LINE (not just a chatbot)
- User asks about LIFF vs MINI App tradeoffs
- User needs AWS CDK deployment for LINE services

---

## Sitthi Thiammekha (สิทธิ เทียมเมฆา) — Flex Message & LIFF Specialist

**Country:** Thailand | **GitHub:** [kamnan43](https://github.com/kamnan43) | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-sitthi-thiammekha/)

**Core expertise:** Flex Message complex layouts, LIFF, LINE MINI App, LINE Pay, NLP integration

**Key contributions:**
- **World Cup LINE Bot** — landmark Flex Message implementation for structured sports data display; became a widely-cited reference project
- Led **LINE MINI App Ignition Bootcamp** in Thailand
- 8+ in-depth articles on LIFF security, Dialogflow integration, LINE Pay API
- Founded **Mekha Innovation** / works at **Emetworks** (EX10 CRM platform for LINE OA)
- 20 years of software development experience

**Design tendency:** Use Flex Message to present data-rich, structured information. Combine multiple LINE services (Messaging + LIFF + Pay) into complete business solutions.

**Reference when:**
- User needs to design information-dense Flex Message layouts (tables, scores, dashboards)
- User asks about LIFF security best practices
- User wants to integrate LINE Pay or build LINE MINI App
- User needs NLP/Dialogflow + LINE Bot integration

---

## Jirawat Karanwittayakarn (จิรวัฒน์) — Firebase Integration & Rich Menu

**Country:** Thailand | **GitHub:** [jirawatee](https://github.com/jirawatee) | **Medium:** [jirawatee](https://jirawatee.medium.com/)

**Core expertise:** LINE Bot + Firebase, Rich Menu management, serverless architecture

**Key contributions:**
- LINE Thailand official **Technology Evangelist**
- Runs **LINE Developers Thailand** Medium publication — the canonical Thai-language LINE Bot resource
- Public repos for LINE Bot + **Firebase Cloud Functions** integration patterns
- Comprehensive tutorial series on message types, user profile APIs, Rich Menu setup
- Founded Thailand's largest Firebase developer group (12,000+ members)
- Google Developer Expert (Firebase)

**Design tendency:** Serverless-first with Firebase. Detailed step-by-step implementation. Rich Menu as primary UX entry point.

**Reference when:**
- User asks about serverless LINE Bot deployment (Firebase/Cloud Functions)
- User needs Rich Menu design and management guidance
- User wants Firebase backend integration (Firestore, Cloud Functions, Authentication)
- User asks about Share Target Picker or LIFF URL handling
- User is looking for beginner-friendly step-by-step implementation

---

## Dr. Winn Voravuthikunchai — AI/NLP for LINE Chatbot

**Country:** Thailand | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-winn-voravuthikunchai/)

**Core expertise:** Thai-language NLP, machine learning, AI chatbot architecture, LLM integration

**Key contributions:**
- Founder & CEO of **Botnoi Group** — Thailand's leading AI chatbot company
- PhD in AI from Caen University (France)
- Former Chief Data Scientist at Telenor
- **Botnoi chatbot** — 1M+ LINE friends in under a year; won international award from LINE Japan for NLP technology
- Integrates **Typhoon LLM** (Thai local AI model), Gemini, and OpenAI with LINE chatbots

**Design tendency:** AI-first chatbot design. Use NLP/LLM as the intelligence layer, LINE Messaging API as the delivery channel. Thai-language optimization for local context.

**Reference when:**
- User wants to integrate LLM/AI into LINE Bot (ChatGPT, Gemini, local models)
- User needs NLP for Thai or non-English language chatbots
- User asks about AI chatbot architecture patterns
- User is building a chatbot that needs to understand natural language, not just keywords

---

## Punsiri Boonyakiat — Enterprise E-commerce & AI

**Country:** Thailand | **Profile:** [LINE API Expert](https://developers.line.biz/en/community/api-experts/th-punsiri-boonyakiat/)

**Core expertise:** Retail e-commerce LINE chatbot, GCP Vertex AI, RAG architecture, enterprise data engineering

**Key contributions:**
- Lead Data Engineer at **Central Food Retail Group (Tops)**
- Part of team behind **Krungthai Connext** LINE chatbot — won LINE Thailand Award 2020
- Presented "The Future of Retail E-commerce with Gemini AI" at LINE DEVCONF 2024 (Vertex AI + RAG)
- Presented on AI Agents + LINE Bot MCP Server
- Google Cloud Certified Professional Data Engineer

**Design tendency:** Enterprise-grade architecture. GCP-native (Vertex AI, BigQuery). Use RAG patterns for product catalog search and customer service automation.

**Reference when:**
- User is building an e-commerce or retail LINE chatbot
- User asks about RAG (Retrieval-Augmented Generation) with LINE Bot
- User needs enterprise-scale LINE Bot architecture (not hobby projects)
- User wants GCP / Vertex AI integration with LINE

---

## Tokuhiro Matsuno — LINE SDK Architecture

**Country:** Japan | **GitHub:** [tokuhirom](https://github.com/tokuhirom)

**Core expertise:** LINE SDK internal architecture, multi-language SDK design, LINE platform services

**Key contributions:**
- LINE Corp (LY Corporation) engineer — designs the APIs that all SDK maintainers implement
- Implemented the **httphandler/webhook module** in line-bot-sdk-go
- Contributor to **line-bot-sdk-python** and other official SDKs
- Developed core LINE services: LINE Customer Connect, LINE Notify, LINE Schedule
- Interviewed the creator of Flex Message for LINE Engineering blog
- Polyglot: Kotlin, Rust, Python, Go

**Design tendency:** API-first design. Build clean internal abstractions that translate consistently across multiple SDK languages. Platform-level thinking over application-level.

**Reference when:**
- User asks about LINE SDK internals or why an API works a certain way
- User needs to understand webhook handler architecture
- User is generating a custom SDK from LINE's OpenAPI specs
- User encounters undocumented API behavior and needs platform-level context

---

## Noda Daisuke (野田大介) — Narrowcast & Audience Segmentation

**Country:** Japan | **Program:** [LINE Frontliner](https://www.lycbiz.com/jp/partner/linefrontliner/) (1st cohort, 2020)

**Core expertise:** LINE OA segment delivery, audience management, Narrowcast targeting for retail/EC

**Key contributions:**
- CEO of Fanatic Inc.
- Built **WazzUp!** — a segment delivery tool for LINE OA that enables CRM without requiring ID linking or member registration
- WazzUp! supports cart-abandonment notifications, restock alerts, and demographic-based Narrowcast via LINE
- Speaker at LINE for Business seminars
- Publishes on note.com about segment delivery strategies for e-commerce and retail

**Design tendency:** Make audience segmentation accessible without heavy ID-linking infrastructure. Use Narrowcast API for targeted delivery based on behavioral signals rather than explicit user registration.

**Reference when:**
- User asks about Narrowcast implementation or audience segmentation strategy
- User needs to build targeted messaging without requiring LINE Login ID linking
- User wants cart-abandonment or restock notification workflows via LINE
- User asks about audience.md APIs (create/update/delete audience groups)

---

## Jin Hsueh (薛覲) — Marketing Analytics & Data Platform

**Country:** Taiwan | **Company:** [Crescendo Lab](https://www.cresclab.com/)

**Core expertise:** LINE marketing data analytics, cross-channel customer journey, conversion tracking, MarTech platform

**Key contributions:**
- Co-founder & CEO of **Crescendo Lab** — LINE Gold-level Technology Partner
- Built **MAAC (Marketing Automation for All Channels)** — serving 500+ brands (IKEA, Starbucks, Rakuten, H&M, adidas)
- MAAC provides cross-channel data analytics, customer journey insights, and conversion tracking on LINE
- Duke University Engineering Management graduate; previously at Red Hat and Deloitte
- Active speaker on LINE MarTech at LINE Biz events in Taiwan, Thailand, Japan

**Design tendency:** Data-driven marketing decisions. Cross-channel analytics (LINE + web + app). Measure ROI of LINE messaging campaigns through conversion tracking and customer journey mapping.

**Reference when:**
- User asks about LINE message delivery analytics or insights API usage
- User needs to track conversion rates or ROI of LINE campaigns
- User asks about follower demographics or user interaction statistics
- User wants to build analytics dashboards from insights.md API data

---

## Tsutsumi Takehiro (堤建拓) — LINE OA Campaign & Coupon Strategy

**Country:** Japan | **Company:** [MARKELINK](https://markelink.biz/)

**Core expertise:** LINE OA coupon campaigns, promotional mechanics, step message automation, LINE OA operations

**Key contributions:**
- CEO of MARKELINK; L-step (Lステップ) certified trainer
- Author of **4 books on LINE OA**, including Japan's first LINE OA book (2019)
- Published **「世界一わかりやすい LINE公式アカウントマスター養成講座」** (9 printings)
- Published **「LINE公式アカウント史上最強の成功テクニック」**
- Supported **600+ companies** in LINE OA and L-step implementation
- Covers coupon flows, loyalty step-ups, and automated promotional sequences

**Design tendency:** Campaign-first design. Build coupon and reward workflows that drive repeat purchases. Use step messages and conditional branching for automated promotional sequences.

**Reference when:**
- User asks about LINE coupon API usage or promotional campaign design
- User needs coupon creation/distribution strategy (coupon.md APIs)
- User wants to design loyalty programs or step-up reward flows via LINE
- User asks about LINE OA marketing automation workflows

---

## Notable Mentions

| Name | Country | Why notable |
|------|---------|-------------|
| **Yuichi Ono (小野侑一)** | Japan | **Creator of Flex Message** at LINE Corp. Designed the CSS Flexbox-based layout system, chose Yoga rendering engine |
| **Thor Kobayashi** | Japan | Created **L Menu Plus** (Rich Menu creation service, 250K users). Rich Menu UX design specialist |
| **Sumihiro Kagawa (加川澄廣)** | Japan | LINE API Expert, Chief Judge of LINE DC BOT AWARDS 2024. LIFF & LINE MINI App expertise |
| **Noriko Matsumoto (松本典子)** | Japan | Designer + Microsoft MVP. No-code LINE Bot via Azure Logic Apps / Power Automate. Reaches non-engineer audiences |
| **Masao Wakasa (若狭正生)** | Japan | First-generation LINE API Expert. LINE BOT AWARDS Geek Award winner (Shakure). Art-tech creative projects, International Digital Emmy nominee |
| **Yosuke Inoue (井上陽介)** | Japan | Youngest LINE API Expert. Built a LINE Bot in high school used by 80% of his grade. Youth education advocate |
| **Thepnatee Phojan (Oa)** | Thailand | LINE API Expert at Emetworks (with Sitthi). LINE MINI App + AWS/GCP deployment. Co-presented TicketO at DEVCONF 2025 |
| **Supakarn Laorattanakul (Prompt)** | Thailand | LINE API Expert. Full-stack (React/Next.js/NestJS). LINE HACK 2020 winner. Modern frontend for MINI App |
| **Thomson Ounapant** | Thailand | LINE API Expert. Trained 62+ SME businesses in LINE OA. YouTube channel "iton5". Bridges developers and business users |
| **Traitanit Huangsri** | Thailand | LINE Thailand Lead Solution Engineer. Cypress.io Thailand founder (3,000+ members). Built Flex Message football bot |
| **Cheng-Lung Sung (宋政隆)** | Taiwan | LINE API Expert. Go + Python + NLP + Machine Learning. AI intelligence layer for chatbots |
| **Caesar Chi (紀創維)** | Taiwan | LINE API Expert. Node.js e-commerce chatbot specialist. JSDC Taiwan core member. Founded Exma-Square |
| **David Tung (董大偉)** | Taiwan | LINE API Expert. Microsoft Regional Director, 15-year MVP. C#/.NET LINE Bot. Published 10+ tech books |
| **Kuan-Hung Kuo (郭冠宏)** | Taiwan | LINE API Expert. Connected to **Cofacts (真的假的)** — g0v civic tech fact-checking LINE Bot, 300K+ users. NLP/NLU |
| **Nur Rohman** | Indonesia | LINE API Expert. CPO at Dicoding Indonesia. Built LINE Academy education platform. Samsung Developer Warrior |
| **M Gilang Januar** | Indonesia | LINE API Expert. Co-creator of **Kerang Ajaib** bot (650K+ followers, group chat entertainment bot). Applied AI Engineer |
| **Soesapto Joeni Hantoro** | Indonesia | LINE API Expert. Created **Othello multiplayer game bot** (230K+ adders) — innovative group chat game using image map |
| **Takubo Hiroshi (田窪洋士)** | Japan | Creator of **L-step (Lステップ)** — Japan's dominant LINE OA marketing automation tool. Step messages, conditional branching, customer scoring |
| **Okada Kazahaya (岡田風早)** | Japan | CEO of SocialPLUS. Pioneered **LINE ID-linked CRM** for e-commerce. Shopify-LINE integration (CRM PLUS on LINE) |
| **Ogawa Hideto (小川秀人)** | Japan | LINE OA coupon campaign specialist. Publishes detailed playbooks on step-up coupons, gamified campaigns, promotional mechanics |
| **Roy Lo (羅建凱)** | Taiwan | Co-founder of **BotBonnie** (acquired by Appier). Chatbot-driven marketing automation on LINE |
| **Chen Tzu-Lung (陳子龍)** | Taiwan | Co-founder of **Super 8 Studio**. Social CRM and conversational marketing on LINE. Agentic AI as a Service |
| **Alan Chan** | HK/Taiwan | Founder of **Omnichat**. Omnichannel chat commerce platform, LINE Technology Partner. 5,000+ brands |
| **Kenichiro Nakamura** | Japan | LINE API Expert. Principal PM at Microsoft. Co-developed **LINE Messaging API SDK for C#**. Co-authored LINE API実践ガイド |

---

## How to Use This Reference

1. When a user's question matches an expert's domain, consider their documented approach
2. Reference their actual open-source projects as examples when relevant
3. Never fabricate opinions or statements attributed to these individuals
4. Use their contributions as evidence of proven patterns, not as authority arguments
