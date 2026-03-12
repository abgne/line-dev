# Group Chat APIs

## Concepts

LINE has two types of multi-user chats:

| | Group Chat | Multi-person Chat (Room) |
|---|-----------|--------------------------|
| ID prefix | `groupId` (C...) | `roomId` (R...) |
| Name/icon | User-defined | Auto-set from member names |
| Albums & Notes | Supported | Not supported |
| Summary API | Available | Not available |
| Status | **Active — all new multi-user chats are groups** | **Legacy — merged into groups since LINE v10.17.0** |

Existing rooms remain functional, but no new rooms are created. Design for group chats as the primary scenario; handle rooms only for backward compatibility.

## Prerequisites

- **Enable "Allow bot to join group chats"** in the Messaging API channel settings on LINE Developers Console
- Only **one LINE Official Account** can be added per chat
- The bot receives webhook events (message, join, leave, memberJoined, memberLeft) with `source.groupId` or `source.roomId`

## Sending Messages to Group Chats

- **Reply message**: Use `replyToken` from webhook events (same as 1:1)
- **Push message**: Set `to` = `groupId` or `roomId` — message is visible to all members
- **Multicast is NOT supported** for group/room IDs — use push instead
- **Broadcast** goes to all friends in 1:1, not to groups

## Group Chat Endpoints

All require `Authorization: Bearer {channel access token}`. Rate limit: **2,000 req/sec**.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get summary | GET | `/v2/bot/group/{groupId}/summary` |
| Get member count | GET | `/v2/bot/group/{groupId}/members/count` |
| Get member IDs | GET | `/v2/bot/group/{groupId}/members/ids` |
| Get member profile | GET | `/v2/bot/group/{groupId}/member/{userId}` |
| Leave | POST | `/v2/bot/group/{groupId}/leave` |

## Room Endpoints (Legacy)

Same response structure as group endpoints. Rate limit: **2,000 req/sec**.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get member count | GET | `/v2/bot/room/{roomId}/members/count` |
| Get member IDs | GET | `/v2/bot/room/{roomId}/members/ids` |
| Get member profile | GET | `/v2/bot/room/{roomId}/member/{userId}` |
| Leave | POST | `/v2/bot/room/{roomId}/leave` |

## Response Details

### Get Summary (Group only)

```json
{
  "groupId": "Ca56f94637c...",
  "groupName": "Group Name",
  "pictureUrl": "https://profile.line-scdn.net/..."
}
```

- `pictureUrl`: Not included if the group has no icon.

### Get Member Count

```json
{ "count": 3 }
```

The count **excludes the LINE Official Account** itself. Includes users who haven't added the bot as friend or have blocked it.

### Get Member IDs (Paginated)

**Verified or premium accounts only.**

```json
{
  "memberIds": ["U4af4980629...", "U0c229f96c4...", "U95afb1d4df..."],
  "next": "jxEWCEEP..."
}
```

- Max 100 user IDs per response
- `next`: Continuation token (expires 24 hours). Pass as `start` query parameter for next page. Not included when all IDs have been returned.
- Only users on LINE for iOS and LINE for Android are included (users must consent to profile access)
- Includes users who haven't added the bot as friend or have blocked it

### Get Member Profile

```json
{
  "displayName": "LINE taro",
  "userId": "U4af4980629...",
  "pictureUrl": "https://sprofile.line-scdn.net/..."
}
```

- `pictureUrl`: Not included if the user has no profile image.
- **Can get profile of any member in the chat**, regardless of friend status or blocked status. This differs from [Get User Profile](user.md) which cannot retrieve blocked users.
- Profile may differ from 1:1 chat — users can set group-specific display names.

### Leave

Returns `200` with empty JSON `{}`. **Irreversible** — the bot must be re-invited to rejoin.

## Error Responses

| Code | Description |
|------|-------------|
| `400` | Invalid group/room ID, or invalid user ID, or invalid/expired continuation token |
| `403` | Not authorized — member IDs endpoints require verified or premium account |
| `404` | Non-existent group/room, or bot is not a member, or user not in the chat |
