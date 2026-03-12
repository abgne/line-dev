# User Profile & Bot Linking

## Get User Profile

```
GET https://api.line.me/v2/profile
Authorization: Bearer {access_token}
```

Requires `profile` scope. Only returns main profile (not subprofile).

### Response (200)
```json
{
  "userId": "U1234567890abcdef",
  "displayName": "LINE User",
  "pictureUrl": "https://profile.line-scdn.net/...",
  "statusMessage": "Hello!"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `userId` | String | User's LINE ID (U + 32 hex chars). Unique per provider. |
| `displayName` | String | User's display name |
| `pictureUrl` | String | Profile image URL. May be absent if user has no profile image. |
| `statusMessage` | String | User's status message. May be absent if not set. |

**Important**: Identify users by their `userId` — user IDs cannot be changed. Display names, images, and status messages are mutable and must not be used for identification.

**Note**: `userId` is unique per provider (not per channel). All channels under the same provider share the same `userId` for a given user. The same LINE user authenticated via **different providers** will have **different userIds**.

### Profile Image Thumbnails

Append suffix to `pictureUrl` for thumbnails:
- `/large` — 200x200 pixels
- `/small` — 51x51 pixels

## Link a Bot

LINE Login can prompt users to add your LINE Official Account (bot) as a friend during the login flow.

### Setup
1. The Messaging API channel (linked to the LINE Official Account) and the LINE Login channel must belong to the **same provider**
2. You must have **administrator** access on both the LINE Login channel and the Messaging API channel
3. Link the LINE Official Account to your LINE Login channel in LINE Developers Console
4. One LINE Login channel can link to **one LINE Official Account** only

### bot_prompt Parameter

Add `bot_prompt` to the authorization URL:

| Value | Behavior |
|-------|----------|
| `normal` | Add-friend option shown **on** the consent screen |
| `aggressive` | Add-friend option shown on a **separate screen after** consent |
| (omitted) | No add-friend prompt |

### friendship_status_changed

When bot linking is configured, the authorization response includes `friendship_status_changed`:

```
{redirect_uri}?code={code}&state={state}&friendship_status_changed=true
```

| Value | Meaning |
|-------|---------|
| `true` | User's friendship status changed during this login (added or unblocked the bot) |
| `false` | No change (already friends, or user declined) |

**Note**: `friendship_status_changed` only indicates whether a change occurred during this specific login session. It does not tell you the current friendship status.

**Note**: On certified provider channels, the add-friend option is **selected by default** when using `bot_prompt=normal`.

### Check Friendship Status

```
GET https://api.line.me/friendship/v1/status
Authorization: Bearer {access_token}
```

Requires `profile` scope.

### Response (200)
```json
{
  "friendFlag": true
}
```

| Value | Meaning |
|-------|---------|
| `true` | User is currently friends with the linked bot |
| `false` | User is not friends (never added, or blocked/deleted) |

### Display Logic by User Relationship

| Already friends? | `bot_prompt` shown? | `friendship_status_changed` |
|-----------------|---------------------|---------------------------|
| Yes | No (auto-skipped) | `false` |
| No, user adds | Yes | `true` |
| No, user declines | Yes | `false` |
| Blocked, user unblocks | Yes | `true` |

## Deauthorize

Revoke a user's authorization for your LINE Login channel. Call this when a user unregisters from your service. Also works for LIFF apps and LINE MINI Apps.

```
POST https://api.line.me/user/v1/deauthorize
Authorization: Bearer {channel access token}
Content-Type: application/json
```

### Request Body (JSON)
```json
{
  "userAccessToken": "{user access token}"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `userAccessToken` | Yes | Access token of the target user |

**Note**: The `Authorization` header requires a **channel access token** (v2.1 or stateless, not a user access token). Issue a channel access token from LINE Developers Console or via the Messaging API token endpoint.

Returns `204 No Content` on success.

### Error Response
| Code | Description |
|------|-------------|
| `400` | Invalid user access token. Either the user already deauthorized, or you already deauthorized via API. |

```json
{"message": "invalid token"}
```

After deauthorization:
- User's access token and refresh token become invalid
- User will need to re-authorize on next LINE Login attempt
- User's friendship with the linked bot is **not** affected
