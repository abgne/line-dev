# Account & Users

## User ID

Format: `U[0-9a-f]{32}` (e.g., `U8189cf6745fc0d808977bdb0b9f22995`)

User IDs are consistent across channels **within the same provider** (e.g., Messaging API and LINE Login channels under the same provider share the same user ID). **Different providers generate different user IDs for the same user.**

**Validating a user ID:** Call Get User Profile — `200` means the user is reachable, any other status code means messages cannot be delivered.

## User Consent (Profile Access)

Users grant consent to share profile information when they first use LINE for iOS or Android. **If a user hasn't consented, the bot cannot identify them.** This affects flow design fundamentally.

**Impact on webhooks:**
- `source.userId` in webhook event objects — **not included**
- `mention` object in text messages — **not included**
- `membership` webhook event — **not sent**

**Impact on APIs (user is excluded from results):**
- Get Follower IDs
- Get Group/Room Member IDs
- Get Membership User IDs

**Who can't consent:**
- Users who only use LINE for PC (PC-only account creation stopped April 2020 — rare but possible)

**Design implication:** Always handle the case where `source.userId` may be absent in webhook events. Don't assume every message has an identifiable sender.

## Bot Info

`GET https://api.line.me/v2/bot/info`

Gets the bot's basic information.

Response:
```json
{
  "userId": "Ub9952f8...",
  "basicId": "@216ru...",
  "displayName": "Example name",
  "pictureUrl": "https://profile.line-scdn.net/0hbGgpkVAb...",
  "chatMode": "chat",
  "markAsReadMode": "manual"
}
```

| Property | Type | Description |
|----------|------|-------------|
| `userId` | String | Bot's user ID |
| `basicId` | String | Bot's basic ID |
| `premiumId` | String? | Bot's premium ID. Not included if not set |
| `displayName` | String | Bot's display name |
| `pictureUrl` | String? | Profile image URL (HTTPS). Not included if no profile image |
| `chatMode` | String | `chat` (Chat is On) / `bot` (Chat is Off) |
| `markAsReadMode` | String | `auto` (Chat Off) / `manual` (Chat On) |

Rate limit: 2,000 req/sec

## Get User Profile

`GET https://api.line.me/v2/bot/profile/{userId}`

Gets the profile information of users who meet one of these conditions:
- Users who have added your LINE Official Account as a friend
- Users who haven't added your LINE Official Account as a friend but have sent a message to your LINE Official Account (except users who have blocked)

Cannot get profile of users who have blocked the LINE Official Account. Only the main profile is returned (not subprofile).

For group/room member profiles, use the endpoints in [group-chat.md](group-chat.md).

Response:
```json
{
  "displayName": "LINE taro",
  "userId": "U4af4980629...",
  "language": "en",
  "pictureUrl": "https://profile.line-scdn.net/...",
  "statusMessage": "Hello, LINE!"
}
```

| Property | Type | Description |
|----------|------|-------------|
| `displayName` | String | User's display name |
| `userId` | String | User ID |
| `language` | String? | User's language (BCP 47 tag, e.g., `en`, `zh-TW`). Not included if user hasn't consented to the LY Corporation Privacy Policy |
| `pictureUrl` | String? | Profile image URL (HTTPS). Not included if user has no profile image |
| `statusMessage` | String? | User's status message. Not included if user has no status message |

**Error responses:**

| Code | Description |
|------|-------------|
| `400` | Invalid user ID |
| `404` | User not found (doesn't exist, hasn't consented, not a friend, or blocked) |

Rate limit: 2,000 req/sec

## Get Follower IDs

`GET https://api.line.me/v2/bot/followers/ids`

Gets the list of user IDs of users who have added your LINE Official Account as a friend.

**Only available for verified or premium accounts.**

Paginate by using the `next` continuation token from the response as the `start` query parameter of the next request. Repeat until `next` is no longer included.

**Query parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `limit` | No | Max user IDs per request (default 300, max 1,000) |
| `start` | No | Continuation token from previous response's `next` property |

Response:
```json
{
  "userIds": ["U4af4980629...", "U0c229f96c4...", "U95afb1d4df..."],
  "next": "yANU9IA..."
}
```

- `next`: Continuation token (expires in 24 hours). Not included when all user IDs have been returned.

**Restrictions on user IDs that can be obtained:**
- Users who deleted their LINE accounts are excluded
- Users who blocked the LINE Official Account are excluded
- Users who haven't consented to profile information being obtained are excluded

**Error responses:**

| Code | Description |
|------|-------------|
| `400` | Invalid continuation token (e.g., expired) |
| `403` | Not authorized — only available for verified or premium accounts |

Rate limit: 2,000 req/sec

## Membership

Membership allows LINE Official Accounts to offer paid subscription plans. Plans are created in LINE Official Account Manager; the API provides read access and member management.

### Get Membership Plans

`GET https://api.line.me/v2/bot/membership/list`

Gets membership plans currently being offered. Plans under review or terminated are excluded.

Response:
```json
{
  "memberships": [
    {
      "membershipId": 3189,
      "title": "Basic Plan",
      "description": "You will receive messages and photos every Saturday.",
      "benefits": ["Members Only Messages", "Members Only Photos"],
      "price": 500.00,
      "currency": "JPY",
      "memberCount": 1,
      "memberLimit": null,
      "isInAppPurchase": true,
      "isPublished": true
    }
  ]
}
```

| Property | Type | Description |
|----------|------|-------------|
| `membershipId` | Number | Membership plan ID |
| `title` | String | Plan name |
| `description` | String | Plan description |
| `benefits` | String[] | List of perks (max 5) |
| `price` | Number | Monthly fee (e.g., `1500.00`) |
| `currency` | String | `JPY` / `TWD` / `THB` |
| `memberCount` | Number | Current subscriber count |
| `memberLimit` | Number? | Max subscribers (`null` if no limit) |
| `isInAppPurchase` | Boolean | `true`: in-app purchase / `false`: browser payment |
| `isPublished` | Boolean | `true`: public / `false`: discontinued but still offering perks |

Max 5 plans per account. Error `404` if no plans offered.

Rate limit: 200 req/sec

### Get User's Membership Subscription

`GET https://api.line.me/v2/bot/membership/subscription/{userId}`

Gets information about the memberships a user has subscribed to.

Response:
```json
{
  "subscriptions": [
    {
      "membership": {
        "membershipId": 3189,
        "title": "Basic Plan",
        "description": "...",
        "benefits": ["Members Only Messages"],
        "price": 500.00,
        "currency": "JPY"
      },
      "user": {
        "membershipNo": 1,
        "joinedTime": 1707214784,
        "nextBillingDate": "2024-02-08",
        "totalSubscriptionMonths": 1
      }
    }
  ]
}
```

| Property | Type | Description |
|----------|------|-------------|
| `membership` | Object | Plan info (same fields as Get Plans: membershipId, title, description, benefits, price, currency) |
| `user.membershipNo` | Number | User's member number in the plan |
| `user.joinedTime` | Number | Subscription time (UNIX seconds) |
| `user.nextBillingDate` | String | Next payment date (`yyyy-MM-dd`, UTC+9) |
| `user.totalSubscriptionMonths` | Number | Months subscribed (resets on re-subscribe) |

**Error responses:**

| Code | Description |
|------|-------------|
| `400` | Invalid user ID |
| `404` | User doesn't subscribe to membership, or user ID doesn't exist |

Rate limit: 200 req/sec

### Get Membership User IDs

`GET https://api.line.me/v2/bot/membership/{membershipId}/users/ids`

Gets user IDs of users who have joined a membership. Same pagination pattern as Get Follower IDs.

**Query parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `limit` | No | Max user IDs per request (default 300, max 1,000) |
| `start` | No | Continuation token from previous response's `next` property |

Response: Same structure as Get Follower IDs (`userIds[]` + optional `next`). Token expires in 24 hours.

**Restrictions:** Same as Get Follower IDs — excludes deleted accounts, blocked users, non-friends, and users who haven't consented to profile access.

**Error responses:**

| Code | Description |
|------|-------------|
| `400` | Invalid continuation token or limit value |
| `404` | Membership ID doesn't exist |

Rate limit: 200 req/sec

## Account Link

Links a LINE user account with an external service account (e.g., existing member system, e-commerce account).

### Issue Link Token

`POST https://api.line.me/v2/bot/user/{userId}/linkToken`

Issues a one-time link token for the account link flow.

Response:
```json
{ "linkToken": "NMZTNuVrPTqlr2IF8Bnymkb7rXfYv5EY" }
```

- Token is **valid for 10 minutes**, single-use
- Validity period may change without notice

**Account link flow:**
1. Bot receives a message/event from user → gets `userId`
2. Bot server calls this endpoint → gets `linkToken`
3. Bot sends user a URL to the provider's login page (include `linkToken` as parameter)
4. User authenticates on the provider's site
5. Provider generates a `nonce` and redirects to `https://access.line.me/dialog/bot/accountLink?linkToken={linkToken}&nonce={nonce}`
6. LINE sends an `accountLink` webhook event to the bot with `result` (`ok`/`failed`) and `nonce`
7. Bot server uses `nonce` to look up the linked external account

**Nonce requirements:**
- Length: **10 to 255 characters**
- Must be one-time and unpredictable — **do not use predictable values** like user IDs
- Minimum entropy: **128 bits** (16 bytes), recommended Base64 encoded
- Store the nonce-to-service-account mapping server-side before redirecting

Rate limit: 2,000 req/sec
