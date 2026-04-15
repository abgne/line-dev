# Audience Management

Audiences allow you to target specific groups of users for narrowcast and broadcast messages.

**Regional restriction:** Only LINE Official Accounts created by users in Japan (JP), Thailand (TH), or Taiwan (TW) can create audiences.

## Specifications

| Item | Limit |
|------|-------|
| Max audiences per channel | 1,000 |
| Retention period | Up to 180 days |
| Max user IDs per request (JSON) | 10,000 |
| Max user IDs per request (file) | 1,500,000 |
| Users per upload audience | No limit |
| Users per click/impression audience | Min 50 |
| Retargeting audience creation window | 60 days after message sent |
| Concurrent operations per audienceGroupId | 10 |

## Audience Types

| Type | Value | Creatable via API | Description |
|------|-------|-------------------|-------------|
| Upload | `UPLOAD` | Yes | User IDs uploaded via API or file |
| Click | `CLICK` | Yes | Users who clicked a URL in broadcast/narrowcast |
| Impression | `IMP` | Yes | Users who viewed a broadcast/narrowcast message |
| Chat tag | `CHAT_TAG` | No | Created via LINE Official Account Manager |
| Friend path | — | No | Created via LINE Official Account Manager |
| Reservation | — | No | Created via LINE Official Account Manager |
| Rich menu impression | `RICHMENU_IMP` | No | Users who viewed a Rich Menu |
| Rich menu click | `RICHMENU_CLICK` | No | Users who clicked a Rich Menu |
| Web traffic (LINE Tag) | `WEBTRAFFIC` | No | Via LINE Official Account Manager or LINE Ads |
| Web traffic (Tracking Tag) | — | No | Created via LINE Official Account Manager |
| App event | — | No | Created via LINE Ads |
| Video view | `VIDEO_VIEW` | No | Created via LINE Ads |
| Image click | — | No | Created via LINE Ads |

## API Endpoints

All require `Authorization: Bearer {channel access token}`.

### Create Audience (Upload)

| Method | Endpoint | Content-Type | Domain |
|--------|----------|--------------|--------|
| POST (JSON) | `/v2/bot/audienceGroup/upload` | `application/json` | `api.line.me` |
| POST (file) | `/v2/bot/audienceGroup/upload/byFile` | `multipart/form-data` | `api-data.line.me` |

**JSON body:**
```json
{
  "description": "Audience name",
  "isIfaAudience": false,
  "uploadDescription": "job description",
  "audiences": [
    {"id": "U4af4980627..."},
    {"id": "U4af4980628..."}
  ]
}
```

**File body (multipart):**
- `description` (required): Audience name (max 120 chars)
- `isIfaAudience` (optional): `true` for IFA, `false` (default) for user IDs
- `uploadDescription` (optional): Job description (max 300 chars)
- `file` (required): Text file, one user ID per line (`text/plain`, max 1,500,000)

Response: `202` with `audienceGroupId`. Audience is created asynchronously — check status before use.

Notes:
- If `audiences` is omitted or empty, an empty audience is created (`audienceCount` = 0, status stays `IN_PROGRESS`, can't accept messages)
- IFA-based audiences require corporate application — contact LINE sales representative
- To verify user IDs before upload, use [Get Profile](user.md) — valid IDs return `200`

### Add User IDs to Audience

| Method | Endpoint | Content-Type | Domain |
|--------|----------|--------------|--------|
| PUT (JSON) | `/v2/bot/audienceGroup/upload` | `application/json` | `api.line.me` |
| PUT (file) | `/v2/bot/audienceGroup/upload/byFile` | `multipart/form-data` | `api-data.line.me` |

**JSON body:**
```json
{
  "audienceGroupId": 4389303728991,
  "uploadDescription": "fileName",
  "audiences": [{"id": "U4af4980627..."}]
}
```

Important:
- Cannot switch between user IDs and IFAs after creation
- Cannot delete user IDs or IFAs once added
- Only users who agreed to LY Corporation Privacy Policy will be added
- Recommended request timeout: 30 seconds or more

### Create Click Audience

`POST https://api.line.me/v2/bot/audienceGroup/click`

```json
{
  "description": "Audience name",
  "requestId": "bb9744f9-47fa-4a29-941e-1234567890ab",
  "clickUrl": "https://example.com/"
}
```

- `requestId` (required): Request ID from a broadcast/narrowcast sent within 60 days (from `X-Line-Request-Id` response header). Push/reply/multicast request IDs cannot be used.
- `clickUrl` (optional): Specific URL. If omitted, users who clicked any URL are included. Max 2,000 chars.

### Create Impression Audience

`POST https://api.line.me/v2/bot/audienceGroup/imp`

```json
{
  "description": "Audience name",
  "requestId": "bb9744f9-47fa-4a29-941e-1234567890ab"
}
```

- `requestId` (required): Same rules as click audience.

### Get / List / Rename / Delete

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get data | GET | `/v2/bot/audienceGroup/{audienceGroupId}` |
| List | GET | `/v2/bot/audienceGroup/list?page=1&size=40` |
| Rename | PUT | `/v2/bot/audienceGroup/{audienceGroupId}/updateDescription` |
| Delete | DELETE | `/v2/bot/audienceGroup/{audienceGroupId}` |

**Get data** returns audience details and `jobs[]` array tracking upload progress:

```json
{
  "audienceGroup": {
    "audienceGroupId": 1234567890123,
    "createRoute": "MESSAGING_API",
    "type": "UPLOAD",
    "description": "Audience name",
    "status": "READY",
    "audienceCount": 1887,
    "created": 1608617466,
    "permission": "READ_WRITE",
    "isIfaAudience": false,
    "expireTimestamp": 1624342266
  },
  "jobs": [
    {
      "audienceGroupJobId": 12345678,
      "audienceGroupId": 1234567890123,
      "description": "audience_list.txt",
      "type": "DIFF_ADD",
      "failedType": null,
      "audienceCount": 0,
      "created": 1608617472,
      "jobStatus": "FINISHED"
    }
  ]
}
```

**Audience status values:**

| Status | Description |
|--------|-------------|
| `IN_PROGRESS` | Pending (may take hours). For UPLOAD audiences, stays here only when `audiences` was omitted/empty at creation — not because the count is < 50. For CLICK/IMP and other restricted types, stays here until the count reaches their minimum (e.g., 50) |
| `READY` | Ready for messaging |
| `FAILED` | Creation error |
| `EXPIRED` | Expired (auto-deleted 1 month later) |
| `INACTIVE` | Inactive |
| `ACTIVATING` | Activating |

**Job status values:** `QUEUED`, `WORKING`, `FINISHED`, `FAILED`

**List query parameters:**
- `page` (required): Page number (1-based)
- `description` (optional): Search by name (partial, case-insensitive)
- `status` (optional): Filter by status
- `size` (optional): Results per page (default 20, max 40)

**Delete** is irreversible. Confirm the audience is no longer in use before deleting.

### Rate Limits

All audience endpoints: **60 req/min** (12 endpoints total). Additional concurrency limit of **10 parallel requests** per audienceGroupId.

## Conditions for Users Added to Audience

Users who are friends with the LINE Official Account can be added. Even if `202` is returned, these users are included but messages won't be sent to them:
- Users who deleted their LINE account
- Users who blocked the LINE Official Account
- Users who haven't added the LINE Official Account as a friend

## Business Manager (Shared Audiences)

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get shared audience | GET | `/v2/bot/audienceGroup/{audienceGroupId}` (with Business Manager scope) |
| List shared audiences | GET | `/v2/bot/audienceGroup/list` (with Business Manager scope) |

Shared audiences from LINE Ads or LINE Official Account Manager may have `createRoute` values: `OA_MANAGER`, `AD_MANAGER`, `POINT_AD`.

## Error Details

Error messages returned in `details[].message` of the JSON response:

| Message | Description |
|---------|-------------|
| `AUDIENCE_GROUP_CAN_NOT_UPLOAD_STATUS_EXPIRED` | Audience expired (>180 days since creation) |
| `AUDIENCE_GROUP_COUNT_MAX_OVER` | Max 1,000 audiences already created |
| `AUDIENCE_GROUP_NAME_SIZE_OVER` | Name too long |
| `AUDIENCE_GROUP_NAME_WRONG` | Name contains invalid characters (e.g., `\n`) |
| `AUDIENCE_GROUP_NAME_EMPTY` | Name is empty or only spaces |
| `AUDIENCE_GROUP_NOT_FOUND` | Audience not found |
| `AUDIENCE_GROUP_REQUESTID_DUPLICATE` | Duplicate request ID |
| `AUDIENCE_GROUP_UPLOAD_DESCRIPTION_SIZE_OVER` | Description too long |
| `REQUEST_NOT_FOUND` | Incorrect request ID or LINE not ready |
| `TOO_OLD_MESSAGES` | Message request ID is over 60 days old |
| `UPLOAD_AUDIENCE_GROUP_INVALID_AUDIENCE_ID_FORMAT` | Invalid user ID or IFA in `audiences[].id` or `file` |
| `UPLOAD_AUDIENCE_GROUP_NO_VALID_AUDIENCE_IDS` | No valid user ID or IFA found |
| `UPLOAD_AUDIENCE_GROUP_TOO_MANY_AUDIENCE_IDS` | Exceeded max user IDs or IFAs |
| `WRONG_BOT_ID` | Bot ID in request ID doesn't match the channel |
| `ALREADY_ACTIVE` | Audience group is already active |

**Handling `INVALID_AUDIENCE_ID_FORMAT`:** Use [Get Profile](user.md) to validate each user ID. Exclude any that don't return `200`, then retry.
