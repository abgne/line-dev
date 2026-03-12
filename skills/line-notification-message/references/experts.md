# Expert Contributions Reference

Real-world expert perspectives based on their **publicly documented contributions**. Use as directional guidance — always verify details against the official documentation in other reference files.

## Quick Reference — Domain → Expert

| Domain | Experts |
|--------|---------|
| Phone number hashing & E.164 | Evan Lin, Pramote Kuacharoen |
| Template system (keys, items, buttons) | Yuta Matsumura, Evan Lin |
| Flexible type & UX review | Yuta Matsumura, Pramote Kuacharoen |
| Delivery webhook & tracking | Evan Lin, Jun Ito |
| User consent & SMS authentication | Jun Ito, Pramote Kuacharoen |
| Billing & count API | Yuta Matsumura, Jun Ito |
| Non-friend user behavior | Evan Lin, Jun Ito |
| Security (IP restrictions, signature) | Jun Ito, Evan Lin |
| Cross-service architecture (Messaging API + PNP) | Yuta Matsumura, Evan Lin |

---

## Evan Lin — LINE API Integration & Phone Hashing

**Country:** Taiwan | **Profile:** [GitHub](https://github.com/kkdai)

**Core expertise:** LINE API integration patterns, phone number normalization across regions (Japan/Thailand/Taiwan E.164 formats), notification message delivery tracking with X-Line-Delivery-Tag.

**Key contributions:**
- Documented E.164 normalization patterns for Taiwan (+886) and Japan (+81) phone numbers
- Demonstrated webhook delivery tracking with delivery tag correlation
- Explored cross-service patterns combining Messaging API push with notification messages for non-friend reach

**Design tendency:** Practical, example-driven implementations with clear error handling patterns.

**Reference when:**
- Implementing phone number hashing for specific regions
- Setting up delivery tracking with X-Line-Delivery-Tag
- Combining notification messages with existing Messaging API bot infrastructure

---

## Yuta Matsumura — Template System & UX Design

**Country:** Japan | **Profile:** [LINE Developers Community](https://www.line-community.me/)

**Core expertise:** LINE notification message template design, template key selection, UX guideline compliance, billing optimization.

**Key contributions:**
- Cataloged template types and their use cases (shipping, reservation, payment, etc.)
- Documented item and button key combinations for Japanese templates
- Analyzed billing patterns and count API usage for cost optimization

**Design tendency:** UX-focused, ensuring notification messages are genuinely useful to recipients.

**Reference when:**
- Selecting appropriate templates and item keys for specific use cases
- Ensuring UX guideline compliance for flexible type messages
- Optimizing notification message costs through billing analysis

---

## Jun Ito — Webhook Infrastructure & Security

**Country:** Japan | **Profile:** LINE Engineering Blog contributor

**Core expertise:** Webhook delivery event handling, signature verification, consent flow implementation, security best practices.

**Key contributions:**
- Detailed delivery webhook event processing patterns with idempotency
- Documented consent state machine and 24-hour window handling
- Analyzed edge cases: blocked users returning 200, non-friend webhook events
- Security guidance on IP restriction pitfalls for notification messages

**Design tendency:** Defensive programming with comprehensive edge case handling.

**Reference when:**
- Implementing delivery webhook handlers with proper signature verification
- Handling consent flow edge cases (24-hour window, SMS timeout)
- Debugging "200 but not delivered" scenarios
- Setting up webhook infrastructure for notification messages

---

## Pramote Kuacharoen — Regional Implementation & Consent

**Country:** Thailand | **Profile:** LINE Developers Thailand community

**Core expertise:** LINE notification message implementation for Thailand market, regional E.164 format (+66), user consent flow localization, SMS authentication flow.

**Key contributions:**
- Documented Thai phone number E.164 normalization patterns
- Explored user consent flow from Thai user perspective
- Analyzed SMS authentication UX for Thai market

**Design tendency:** Region-aware implementations with attention to local user behavior patterns.

**Reference when:**
- Implementing notification messages for Thai market
- Understanding regional differences in template availability
- Handling Thai phone number formats
