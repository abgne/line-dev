# Rich Menu

Customizable menu displayed at the bottom of the LINE Official Account chat screen. **Not available on LINE for PC (macOS/Windows)** — mobile only.

## Display Priority (Highest → Lowest)

1. **Per-user rich menu** set via Messaging API — **takes effect immediately**
2. **Default rich menu** set via Messaging API — takes effect when user reopens chat (up to 1 min delay)
3. **Default rich menu** set via LINE Official Account Manager — takes effect when user reopens chat

Per-user always overrides default. If none is set, no rich menu is displayed.

**Key behaviors:**
- Default rich menus are shown to **non-friends** too. Per-user rich menus **cannot** be linked to non-friends
- **Deleting** a rich menu doesn't immediately remove it from user's screen (requires chat reopen). **Unlinking** takes effect immediately
- API-created rich menus have **no statistics** (display count, click rate). OA Manager-created menus do
- OA Manager supports **display period** settings; API does not
- OA Manager does NOT support `postback`, `datetimepicker`, or `richmenuswitch` actions

## Limits

| Item | Limit |
|------|-------|
| Rich menus per channel | 1,000 |
| Rich menu aliases per channel | 1,000 |
| Areas per rich menu | 20 |
| Create rich menu rate limit | **100 req/hr** |
| Delete rich menu rate limit | **100 req/hr** |
| Delete alias rate limit | **100 req/hr** |
| Batch operations rate limit | **3 req/hr** |
| All other endpoints | 2,000 req/sec |

## Rich Menu Object

```json
{
  "size": {"width": 2500, "height": 1686},
  "selected": false,
  "name": "Nice rich menu",
  "chatBarText": "Tap to open",
  "areas": [
    {
      "bounds": {"x": 0, "y": 0, "width": 2500, "height": 1686},
      "action": {"type": "postback", "data": "action=buy&itemid=123"}
    }
  ]
}
```

| Property | Type | Description |
|----------|------|-------------|
| `size` | Object | `{width, height}`. Width: 800–2500px, Height: ≥250px, **aspect ratio (w/h) ≥ 1.45** |
| `selected` | Boolean | `true` to display expanded by default |
| `name` | String | Internal name (not shown to users). Max 300 chars |
| `chatBarText` | String | Text shown in the chat bar. **Max 14 chars** |
| `areas` | Array | Tappable areas. Max 20. Each has `bounds` ({x, y, width, height} in px, origin top-left) and `action` |

**Standard sizes:**

| Type | Dimensions |
|------|-----------|
| Full (HD) | 2500 × 1686 |
| Full (SD) | 1200 × 810 |
| Full (Compact) | 800 × 540 |
| Half (HD) | 2500 × 843 |
| Half (SD) | 1200 × 405 |
| Half (Compact) | 800 × 270 |

**Supported action types:** `postback`, `message`, `uri`, `datetimepicker`, `richmenuswitch`, `clipboard`. Full specs → [action-objects.md](action-objects.md)

## Image Specifications

| Item | Spec |
|------|------|
| Format | JPEG or PNG |
| Max file size | 1 MB |
| Width | 800–2500 px |
| Height | ≥ 250 px |
| Aspect ratio | ≥ 1.45 |
| Domain | **`api-data.line.me`** (not `api.line.me`) |

**Cannot replace** an image once uploaded — must create a new rich menu and re-upload.

## Endpoints

All require `Authorization: Bearer {channel access token}`.

### Rich Menu CRUD

| Operation | Method | Endpoint | Note |
|-----------|--------|----------|------|
| Create | POST | `/v2/bot/richmenu` | Returns `richMenuId`. 100 req/hr |
| Validate | POST | `/v2/bot/richmenu/validate` | Dry-run, returns `{}` if valid |
| Upload image | POST | `api-data.line.me` `/v2/bot/richmenu/{richMenuId}/content` | Content-Type: `image/jpeg` or `image/png` |
| Download image | GET | `api-data.line.me` `/v2/bot/richmenu/{richMenuId}/content` | Returns binary |
| Get | GET | `/v2/bot/richmenu/{richMenuId}` | Returns rich menu response object |
| List | GET | `/v2/bot/richmenu/list` | **Only API-created menus** (not OA Manager) |
| Delete | DELETE | `/v2/bot/richmenu/{richMenuId}` | 100 req/hr |

### Default Rich Menu

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Set default | POST | `/v2/bot/user/all/richmenu/{richMenuId}` |
| Get default ID | GET | `/v2/bot/user/all/richmenu` |
| Clear default | DELETE | `/v2/bot/user/all/richmenu` |

Get default returns `403` if set by another channel (e.g., OA Manager), `404` if not set.

### Per-user Rich Menu

| Operation | Method | Endpoint | Note |
|-----------|--------|----------|------|
| Link to user | POST | `/v2/bot/user/{userId}/richmenu/{richMenuId}` | Replaces existing |
| Link to multiple | POST | `/v2/bot/richmenu/bulk/link` | Async `202`, max 500 userIds |
| Get user's menu | GET | `/v2/bot/user/{userId}/richmenu` | Returns `richMenuId` |
| Unlink from user | DELETE | `/v2/bot/user/{userId}/richmenu` | |
| Unlink from multiple | POST | `/v2/bot/richmenu/bulk/unlink` | Async `202`, max 500 userIds |

**Link conditions:** Only works for users who added the bot as friend. Returns `200`/`202` but **silently fails** for:
- Users who deleted their LINE account
- Users who blocked the bot
- Users who haven't added the bot as friend
- User IDs from another channel/provider

**Bulk operations are async** — verify with Get user's menu after bulk link/unlink.

### Batch Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Batch replace/unlink | POST | `/v2/bot/richmenu/batch` |
| Get batch status | GET | `/v2/bot/richmenu/progress/batch?requestId={requestId}` |
| Validate batch | POST | `/v2/bot/richmenu/batch/validate` |

Rate limit: **3 req/hr**. Three operation types:
1. **Replace:** Switch all users from menu A → menu B
2. **Unlink specific:** Unlink all users from a specific menu
3. **Unlink all:** Unlink all users from any linked menu

Multiple operations in one request are processed independently and in parallel per user.

## Rich Menu Alias (Tab Switching)

Aliases enable tab switching via `richmenuswitch` action. Each alias maps an ID string to a `richMenuId`.

| Operation | Method | Endpoint | Rate |
|-----------|--------|----------|------|
| Create | POST | `/v2/bot/richmenu/alias` | 2,000 req/sec |
| Update | POST | `/v2/bot/richmenu/alias/{richMenuAliasId}` | 2,000 req/sec |
| Get | GET | `/v2/bot/richmenu/alias/{richMenuAliasId}` | 2,000 req/sec |
| List | GET | `/v2/bot/richmenu/alias/list` | 2,000 req/sec |
| Delete | DELETE | `/v2/bot/richmenu/alias/{richMenuAliasId}` | 100 req/hr |

**Alias ID format:** Max 32 chars, `a-z`, `0-9`, `_`, `-`. Must be unique per channel. Can only associate with rich menus in the same channel.

**Alias updates may not reflect immediately** due to caching.

### Tab Switching Setup

1. Create Menu A and Menu B (each with `richmenuswitch` areas pointing to each other's alias)
2. Upload images to both
3. Set one as default rich menu
4. Create aliases: `richmenu-alias-a` → Menu A, `richmenu-alias-b` → Menu B

```json
{
  "type": "richmenuswitch",
  "richMenuAliasId": "richmenu-alias-b",
  "data": "switched-to-b"
}
```

**Teardown order (must follow):**
1. Clear default rich menu
2. Delete all aliases
3. Delete rich menus

**Critical behaviors:**
- **Switching makes the target menu a per-user menu** — after a user taps `richmenuswitch`, the target menu is linked as their per-user menu. This means it "sticks" even if you later change the default menu. To reset, you must unlink or delete the per-user menu
- **If the alias doesn't exist, `richmenuswitch` silently fails** — no error is shown to the user, the tap does nothing
- Alias can be **hot-updated** to point to a different `richMenuId` without redeploying menus
- For 3+ tabs: each menu needs N-1 `richmenuswitch` areas pointing to the other tabs' aliases
