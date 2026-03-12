# LIFF Server API (v1)

REST API for programmatic LIFF app management — create, update, list, and delete LIFF apps without using LINE Developers Console.

**Base URL**: `https://api.line.me/liff/v1/apps`

**Authentication**: All endpoints require `Authorization: Bearer {channel access token}` (short-lived or stateless channel access token issued for the LINE Login channel).

> The Server API version is **v1** — independent from the client-side LIFF SDK v2.

---

## 1. Add LIFF App

`POST https://api.line.me/liff/v1/apps`

Create a new LIFF app on the channel. Maximum **30** LIFF apps per channel.

### Request

```
Content-Type: application/json
Authorization: Bearer {channel access token}
```

| Field | Type | Required | Description |
|-------|------|:---:|-------------|
| `view.type` | string | Yes | `"compact"`, `"tall"`, or `"full"` |
| `view.url` | string | Yes | Endpoint URL (HTTPS, no fragments) |
| `view.moduleMode` | boolean | No | `true` hides action button in header (Full size only) |
| `description` | string | No | App name — cannot contain "LINE" or inappropriate content |
| `features.qrCode` | boolean | No | Enable QR code reader (`liff.scanCodeV2()`). Default `false` |
| `permanentLinkPattern` | string | No | `"concat"` for concatenated URL format |
| `scope` | string[] | No | Scopes: `"openid"`, `"email"`, `"profile"`, `"chat_message.write"`. Default: `["profile", "chat_message.write"]` |
| `botPrompt` | string | No | Add friend option: `"normal"`, `"aggressive"`, or `"none"`. Default `"none"` |

### Response (200)

```json
{ "liffId": "1234567890-AbcdEfgh" }
```

### Errors

| Status | Cause |
|--------|-------|
| 400 | Invalid parameter values, or channel already has 30 LIFF apps |
| 401 | Invalid or missing channel access token |

### Example

```bash
curl -X POST https://api.line.me/liff/v1/apps \
  -H "Authorization: Bearer {channel_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "view": { "type": "tall", "url": "https://example.com/myapp" },
    "description": "My LIFF App",
    "scope": ["openid", "profile", "chat_message.write"],
    "features": { "qrCode": true },
    "botPrompt": "aggressive"
  }'
```

---

## 2. Update LIFF App

`PUT https://api.line.me/liff/v1/apps/{liffId}`

Partially update an existing LIFF app. Only specified fields are updated — omitted fields remain unchanged.

### Request

```
Content-Type: application/json
Authorization: Bearer {channel access token}
```

**Path parameter**: `liffId` — ID of the LIFF app to update.

**Body**: same fields as Add LIFF App, all optional. Only include fields you want to change.

### Response (200)

Empty body.

### Errors

| Status | Cause |
|--------|-------|
| 400 | Invalid parameter values |
| 401 | Invalid or missing channel access token |
| 404 | LIFF app not found or belongs to another channel |

### Example

```bash
curl -X PUT https://api.line.me/liff/v1/apps/1234567890-AbcdEfgh \
  -H "Authorization: Bearer {channel_access_token}" \
  -H "Content-Type: application/json" \
  -d '{ "view": { "type": "full" }, "description": "Updated Name" }'
```

---

## 3. Get All LIFF Apps

`GET https://api.line.me/liff/v1/apps`

List all LIFF apps on the channel.

### Request

```
Authorization: Bearer {channel access token}
```

No request body.

### Response (200)

```json
{
  "apps": [
    {
      "liffId": "1234567890-AbcdEfgh",
      "view": {
        "type": "tall",
        "url": "https://example.com/myapp",
        "moduleMode": false
      },
      "description": "My LIFF App",
      "features": {
        "ble": false,
        "qrCode": true
      },
      "permanentLinkPattern": "concat",
      "scope": ["openid", "profile", "chat_message.write"],
      "botPrompt": "aggressive"
    }
  ]
}
```

### Errors

| Status | Cause |
|--------|-------|
| 401 | Invalid or missing channel access token |
| 404 | No LIFF apps on the channel |

---

## 4. Delete LIFF App

`DELETE https://api.line.me/liff/v1/apps/{liffId}`

Remove a LIFF app from the channel.

### Request

```
Authorization: Bearer {channel access token}
```

**Path parameter**: `liffId` — ID of the LIFF app to delete.

### Response (200)

Empty body.

### Errors

| Status | Cause |
|--------|-------|
| 401 | Invalid or missing channel access token |
| 404 | LIFF app not found or belongs to another channel |

---

## Use Cases

- **CI/CD automation**: create or update LIFF apps during deployment (set Endpoint URL to staging/production)
- **Batch management**: script creation of multiple LIFF apps across channels
- **Infrastructure as code**: version-control LIFF app configurations and apply via API
- **Admin tools**: build internal dashboards for LIFF app management without Console access
