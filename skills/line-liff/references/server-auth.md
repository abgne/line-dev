# LIFF Server-side 驗證

## 流程

```
Client (LIFF App)                    Server
─────────────────                    ──────
1. liff.getIDToken()
   → raw JWT string ──────────────→ 2. 驗證 JWT 簽名
                                     3. 解碼取出 claims
                                     4. 建立 session
```

## Client 端

```javascript
// 取得 raw ID Token (JWT)
const idToken = liff.getIDToken();

// 傳送到你的 server
fetch('/api/auth', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ idToken })
});
```

**注意**: 永遠傳送 `liff.getIDToken()` (raw JWT)，不要傳 `liff.getDecodedIDToken()` (已解碼)。

## Server 端驗證

### 方法 1: 呼叫 LINE API 驗證

```
POST https://api.line.me/oauth2/v2.1/verify
Content-Type: application/x-www-form-urlencoded

id_token={raw_id_token}&client_id={channel_id}
```

Response:
```json
{
  "iss": "https://access.line.me",
  "sub": "U1234567890abcdef",
  "aud": "1234567890",
  "exp": 1700000000,
  "iat": 1699999000,
  "name": "LINE User",
  "picture": "https://profile.line-scdn.net/...",
  "email": "user@example.com"
}
```

### 方法 2: 自行驗證 JWT

使用 Channel Secret 作為 HMAC-SHA256 key 驗證簽名：

```python
import jwt

decoded = jwt.decode(
    id_token,
    channel_secret,
    algorithms=['HS256'],
    audience=channel_id,
    issuer='https://access.line.me'
)
user_id = decoded['sub']
name = decoded['name']
email = decoded.get('email')  # 需要 email scope
```

## ID Token Claims

| Claim | 說明 |
|-------|------|
| `iss` | `https://access.line.me` |
| `sub` | 使用者 ID (U 開頭) |
| `aud` | Channel ID |
| `exp` | 過期時間 (Unix timestamp) |
| `iat` | 發行時間 |
| `name` | 顯示名稱 |
| `picture` | 大頭照 URL |
| `email` | Email (需 `email` scope) |

## Alternative: Access Token Verification

If you need the user's profile but don't require ID token claims (email, etc.), you can verify via access token instead. This is a **two-step** process.

### Step 1: Verify the access token

```
GET https://api.line.me/oauth2/v2.1/verify?access_token={access_token}
```

Response:
```json
{
  "scope": "profile",
  "client_id": "1234567890",
  "expires_in": 43200
}
```

**You must verify**:
- `client_id` matches your channel ID
- `expires_in` > 0 (token not expired)

### Step 2: Get user profile

```
GET https://api.line.me/v2/profile
Authorization: Bearer {access_token}
```

Response:
```json
{
  "userId": "U1234567890abcdef",
  "displayName": "LINE User",
  "pictureUrl": "https://profile.line-scdn.net/...",
  "statusMessage": "Hello"
}
```

### ID Token vs Access Token Path

| | ID Token Path | Access Token Path |
|---|---|---|
| Client method | `liff.getIDToken()` | `liff.getAccessToken()` |
| Server steps | 1 request (`POST /oauth2/v2.1/verify`) | 2 requests (verify + get profile) |
| Returns email | Yes (with `email` scope) | No |
| Offline verification | Yes (self-verify JWT with Channel Secret) | No (must call LINE API) |
| Token lifetime | JWT standard expiry | Revoked when LIFF app closes |

**Recommendation**: Prefer the ID token path — it's a single request, supports offline verification, and provides more claims.

---

## 安全注意事項

- Channel Secret 僅在 server 端使用，永不暴露在 client
- 驗證 `aud` 確保 token 是給你的 channel
- 驗證 `exp` 確保 token 未過期
- LIFF uses **HS256** signing (Channel Secret as HMAC key)
- Native LINE Login SDK uses **ES256** — different verification method
- 如需完整的 OAuth 2.1 flow（獨立網站/App 登入），參考獨立的 `line-login` skill
