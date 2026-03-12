# OAuth 2.1 Authorization Code Flow

## Authorization Endpoint

```
GET https://access.line.me/oauth2/v2.1/authorize
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `response_type` | Yes | `code` |
| `client_id` | Yes | Channel ID |
| `redirect_uri` | Yes | Callback URL (must be URL-encoded, must match registered URL) |
| `state` | Yes | Cryptographically random string for CSRF prevention. Must validate on callback. |
| `scope` | Yes | Space-separated: `profile`, `openid`, `email` |
| `nonce` | No | Random string for replay attack prevention. Included in ID Token if provided. |
| `prompt` | No | `consent` — force consent screen. `login` — force re-authentication. `none` — no UI shown (returns error if interaction needed). |
| `max_age` | No | Max seconds since last authentication. If exceeded, re-authentication required. Required for `auth_time` claim in ID Token. |
| `ui_locales` | No | Space-separated BCP 47 language tags (e.g., `en`, `ja`, `zh-TW`) |
| `bot_prompt` | No | `normal` — show add-friend option on consent screen. `aggressive` — show add-friend option on a separate screen after consent. |
| `initial_amr_display` | No | `lineqr` — show QR code login first instead of email |
| `switch_amr` | No | Boolean, default `true`. Set `false` to hide authentication method switching UI. |
| `disable_auto_login` | No | Boolean, default `false`. Set `true` to disable auto login (useful when auto login causes issues). |
| `disable_ios_auto_login` | No | Boolean, default `false`. Set `true` to disable auto login on iOS only. |
| `code_challenge` | No | PKCE code challenge (Base64URL-encoded SHA256 hash of code_verifier) |
| `code_challenge_method` | No | `S256` (only supported method) |
| `response_mode` | No | `query` (default), `form_post`, `query.jwt`, `form_post.jwt`, `jwt`. JWT modes return a signed response. |

### Scope Combinations

| Scope | Data Available |
|-------|----------------|
| `profile` | User profile (userId, displayName, pictureUrl, statusMessage) via access token |
| `openid` | ID Token (sub = userId) |
| `openid profile` | ID Token with `name` and `picture` claims |
| `openid profile email` | ID Token with `name`, `picture`, and `email` claims |
| `email` alone | Not valid — requires `openid` |

**Notes**:
- `email` scope requires `openid`. The `email` claim is only included when the user has a verified email and has granted permission.
- `email` scope requires approval in LINE Developers Console before use.
- The `email` scope is **not** returned in the `scope` property of the token response, even if granted.

## Authentication Methods

LINE Login supports multiple authentication methods, selected automatically by priority:

| Priority | Method | User Interaction | 2FA Required | Notes |
|----------|--------|-----------------|--------------|-------|
| 1 | **Auto Login** | None | No | Requires Universal Links (iOS) / App Links (Android) configured |
| 2 | **SSO** | Minimal ("Continue as") | No | Uses existing LINE session via `access.line.me` cookies |
| 3 | **Email + Password** | Full credentials | **Yes** | Triggered on first login, device change, or browser change |
| 4 | **QR Code** | Scan with LINE app | **Yes** | Can be shown first with `initial_amr_display=lineqr` |

### Two-Factor Authentication (2FA)
- **Required**: email/password login, QR code login
- **Skipped**: auto login, SSO
- **Device Trust**: 2FA can be skipped for **365 days** on trusted devices
- **Trigger conditions**: first login to service, device change, browser change

## Authorization Response

### Success
```
{redirect_uri}?code={AUTHORIZATION_CODE}&state={state}&friendship_status_changed={true|false}
```

- `code`: Authorization code — valid **10 minutes**, **one-time use**
- `state`: Must match the value sent in the authorization request
- `friendship_status_changed`: Included when bot linking is configured

### Error
```
{redirect_uri}?error={error_code}&state={state}&error_description={description}
```

| Error Code | Description |
|------------|-------------|
| `INVALID_REQUEST` | Missing or invalid parameter |
| `ACCESS_DENIED` | User denied consent |
| `UNSUPPORTED_RESPONSE_TYPE` | Unsupported response_type value |
| `INVALID_SCOPE` | Invalid scope value |
| `SERVER_ERROR` | Internal server error |
| `LOGIN_REQUIRED` | Login required (when `prompt=none`) |
| `INTERACTION_REQUIRED` | User interaction required (when `prompt=none`) |

## Token Exchange

```
POST https://api.line.me/oauth2/v2.1/token
Content-Type: application/x-www-form-urlencoded
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `grant_type` | Yes | `authorization_code` |
| `code` | Yes | Authorization code from callback |
| `redirect_uri` | Yes | Must match the authorization request |
| `client_id` | Yes | Channel ID |
| `client_secret` | Yes | Channel Secret |
| `code_verifier` | PKCE only | Original random string (43-128 chars) used to generate code_challenge |

### Response
```json
{
  "access_token": "...",
  "expires_in": 2592000,
  "id_token": "eyJ...",
  "refresh_token": "...",
  "scope": "profile openid",
  "token_type": "Bearer"
}
```

- `id_token` is only included when `openid` scope was requested
- `expires_in` is in seconds (2592000 = 30 days)

## PKCE (Proof Key for Code Exchange)

Recommended for **public clients** (SPA, mobile apps) that cannot securely store a client_secret.

### Flow

1. Generate `code_verifier`: random string, 43-128 characters, charset `[A-Za-z0-9-._~]`
2. Generate `code_challenge`: `BASE64URL(SHA256(code_verifier))` — Base64URL encoding: remove `=` padding, replace `+` with `-`, replace `/` with `_`
3. Send `code_challenge` and `code_challenge_method=S256` in authorization request
4. Send `code_verifier` in token exchange request

**Only `S256` is supported** — plain code challenge is not allowed.

### Example (Node.js)
```javascript
const crypto = require('crypto');

// Generate code_verifier
const codeVerifier = crypto.randomBytes(32)
  .toString('base64url'); // 43 chars

// Generate code_challenge
const codeChallenge = crypto.createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');
```

## OpenID Connect Discovery

```
GET https://access.line.me/.well-known/openid-configuration
```

Returns standard OpenID Connect configuration including supported scopes, endpoints, signing algorithms, and claims.
