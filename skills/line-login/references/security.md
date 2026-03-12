# Security & Development Guidelines

## Security Checklist

### Authorization Request
- **`state` parameter**: Must be cryptographically random (e.g., `crypto.randomBytes(32)`). Always validate on callback by comparing with the stored value. Prevents CSRF attacks.
- **`nonce` parameter**: Use when requesting `openid` scope. Store server-side and validate in ID Token. Prevents replay attacks.
- **`redirect_uri`**: Must use HTTPS. Must exactly match the registered Callback URL (query parameters may be appended). Verify no Open Redirector vulnerability exists if your callback URL accepts arbitrary redirect parameters.

### State Storage
- **`state` must be stored** in a location inaccessible to third parties: server session or cookies protected by same-origin policy.
- A different `state` value must be generated for **every login attempt**, even for the same user.

### Token Handling
- **Channel Secret**: Must be stored server-side only. Never expose in client-side code, JavaScript bundles, or mobile app binaries.
- **Access Token**: Store securely server-side. If passing to client, use secure HTTP-only cookies or equivalent. After verifying, check that `client_id` matches your channel AND `expires_in` is positive.
- **ID Token**: Always verify signature before trusting claims. Never use unverified ID Token data.

### Data Transmission
- **Never transmit user profiles or Channel ID from client to server** — these can be forged. Only transmit access tokens or ID tokens, then verify/decode server-side.
- **Never trust client-side profile data** — always fetch from LINE's API server-side using a verified access token.

### General
- All API communication must use HTTPS/TLS
- Validate `aud` claim in ID Token matches your Channel ID
- Validate `exp` claim is not expired

## Development Guidelines

### Load Testing
- **Do NOT perform load testing** against LINE's authorization or API endpoints. This may result in your channel being suspended.

### User Deauthorization
- When a user unregisters from your service, call the deauthorize endpoint to revoke their LINE Login authorization:
  ```
  POST https://api.line.me/user/v1/deauthorize
  Authorization: Bearer {channel access token}
  Content-Type: application/json
  Body: {"userAccessToken": "{user_access_token}"}
  ```
- Returns `204 No Content` on success. Returns `400` if already deauthorized or invalid token.
- Document this in your terms/conditions near registration functions.

### Logging
Maintain logs for debugging and auditing:

| Log Item | Description |
|----------|-------------|
| Authorization Request | Time of request, all parameters (state, nonce, scope, redirect_uri, etc.) |
| Authorization Response | Receipt time, request method, authorization codes, error responses |
| Token Exchange | Success/failure, error codes |
| ID Token Verification | Algorithm used, claims validated |
| API Calls | Request ID (`x-line-request-id`), timestamp, method, endpoint, status codes |

**Warning**: LINE does not provide logs of authorization requests or LINE Login API requests upon inquiry. You must maintain your own logs.

### Error Handling
- Handle all OAuth error responses (user denial, invalid scope, server errors)
- Implement graceful fallback when LINE Login is unavailable
- Do not expose internal error details to end users

## Auto Login Failure Handling

Auto login can fail in certain scenarios. Handle these cases to prevent login loops.

### Common Causes
1. **Universal Links / App Links malfunction** — LINE app won't launch; falls back to email login. Common triggers: JavaScript-triggered redirects, direct URL entry by users. **Mitigation**: use user-initiated button taps (not automatic redirects) to trigger the authorization URL.
2. **LINE app not installed** — auto login is unavailable
3. **State mismatch** — when auto login fails on the LINE app, the `state` in the callback will **not match** the `state` in the original authorization URL. This is the primary detection signal, but it **cannot distinguish** between auto login failure and CSRF attacks.

### Detection

The `state` parameter mismatch on callback is the only detection method. When detected:
- You cannot tell if it's an auto login failure or a CSRF attack
- Log the mismatch for monitoring before deciding on a response strategy

### Response Strategies

**Strategy 1: Error message with manual retry** (recommended for better UX transparency)
- Show user a "login failed" notification
- Provide a retry link with `disable_auto_login=true`
- Include a link to LINE Help for troubleshooting

**Strategy 2: Silent redirect** (seamless but hides the failure)
- Automatically redirect with `disable_auto_login=true`
- No notification shown to user

### Redirect with `disable_auto_login=true`

```
GET https://access.line.me/oauth2/v2.1/authorize
  ?response_type=code
  &client_id={channel_id}
  &redirect_uri={redirect_uri}
  &state={new_state}
  &scope=profile%20openid
  &nonce={new_nonce}
  &disable_auto_login=true
```

**Note**: Generate new `state` and `nonce` values for the retry request.

## Login Button Design

Components: LINE icon + speech bubble + vertical divider + button text.

### Colors

| Element | State | Color |
|---------|-------|-------|
| Background | Base | `#06C755` |
| Background | Hover | `#06C755` + `#000000` 10% opacity overlay |
| Background | Press | `#06C755` + `#000000` 30% opacity overlay |
| Background | Disabled | `#FFFFFF` |
| Font & Logo | Active | `#FFFFFF` |
| Font & Logo | Disabled | `#1E1E1E` 20% opacity |
| Vertical line | Active | `#000000` 8% opacity |
| Vertical line | Disabled | `#E5E5E5` 60% opacity |
| Border | Disabled | `#E5E5E5` 60% opacity |

### Layout

- **Horizontal padding** (left/right): >= X (X = LINE icon speech bubble width)
- **Vertical padding** (top/bottom): >= X/2
- **Isolation zone**: >= A around the button (A = speech bubble left padding width). No text or graphics in this zone.
- LINE icon aspect ratio must be preserved

### Text

Recommended phrases: "Log in with LINE" (long) / "Log in" (short). No line breaks. Icon-only is allowed.

| Language | Long | Short |
|----------|------|-------|
| English | Log in with LINE | Log in |
| Japanese | LINEでログイン | ログイン |
| Korean | LINE으로 로그인 | 로그인 |
| Thai | เข้าสู่ระบบด้วย LINE | เข้าสู่ระบบ |
| Chinese (Traditional) | 以LINE帳號登入 | 登入 |
| Chinese (Simplified) | 通过LINE登录 | 登录 |
| Indonesian | Masuk dengan LINE | Masuk |
| Arabic | تسجيل الدخول بحساب LINE | تسجيل الدخول |

### Common Mistakes

- Using non-specified colors
- Using outdated LINE icon
- Modifying or using alternative icons
