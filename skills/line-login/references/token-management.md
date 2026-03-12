# Token Management

## Token Validity

| Token | Validity | Notes |
|-------|----------|-------|
| Authorization Code | 10 minutes | One-time use |
| Access Token | 30 days | Can be refreshed |
| Refresh Token | 90 days (from access token issuance) | Same refresh token is returned on refresh |

## Verify Access Token

```
GET https://api.line.me/oauth2/v2.1/verify?access_token={accessToken}
```

### Response (200)
```json
{
  "scope": "profile openid",
  "client_id": "1234567890",
  "expires_in": 2591963
}
```

- `expires_in`: remaining seconds
- Returns `400` if token is invalid or expired:
  ```json
  {"error": "invalid_request", "error_description": "access token expired"}
  ```

### Post-Verification Checks
After a successful verify response, **both** conditions must be met before using the token:
1. `client_id` must match your LINE Login Channel ID
2. `expires_in` must be a positive value

## Refresh Token

```
POST https://api.line.me/oauth2/v2.1/token
Content-Type: application/x-www-form-urlencoded
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `grant_type` | Yes | `refresh_token` |
| `refresh_token` | Yes | Current refresh token |
| `client_id` | Yes | Channel ID |
| `client_secret` | Conditional | Channel Secret. See [client_secret conditional requirement](api-common.md#client_secret-conditional-requirement). |

### Response
```json
{
  "access_token": "new_access_token",
  "expires_in": 2592000,
  "refresh_token": "same_refresh_token",
  "scope": "profile openid",
  "token_type": "Bearer"
}
```

**Notes**:
- The same refresh token is returned (not a new one). Refreshing the access token does not extend the refresh token's validity period. When the refresh token expires (90 days from original access token issuance), the user must log in again.
- This endpoint cannot be used to refresh a Messaging API channel access token.

### Error Response (400)
```json
{"error": "invalid_grant", "error_description": "invalid refresh token"}
```

## Revoke Token

```
POST https://api.line.me/oauth2/v2.1/revoke
Content-Type: application/x-www-form-urlencoded
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `access_token` | Yes | Access token to revoke |
| `client_id` | Yes | Channel ID |
| `client_secret` | Conditional | Channel Secret. See [client_secret conditional requirement](api-common.md#client_secret-conditional-requirement). |

Returns `200` on success (empty body). Revoking an already-revoked or invalid token also returns `200`.

**Notes**:
- When users log out, revoke their access token AND delete all user data from your application.
- This endpoint cannot be used to revoke a Messaging API channel access token.

## Token Revocation by User

Users can revoke consent for your app via **LINE app > Settings > Account > Authorized apps**. When consent is revoked:

- Both access token and refresh token are **immediately invalidated**
- Refresh token cannot be used to obtain a new access token
- If the user re-authorizes later, the same `userId` is returned (user ID is persistent)
- Your app must comply with the [LINE User Data Policy](https://terms2.line.me/LINE_Developers_user_data_policy) when handling user data after revocation

### Handling Revoked vs Expired Tokens

| Scenario | Verify Response | Refresh Possible? |
|----------|----------------|-------------------|
| Token valid | `200` with scope/client_id/expires_in | Yes |
| Token expired | `400` — `"access token expired"` | Yes (if refresh token still valid) |
| Token revoked by user | `400` — `"invalid_request"` | No (refresh token also invalidated) |

When receiving a `400` on token verify or refresh, check whether the user has revoked consent before prompting re-login.

## ID Token (JWT)

ID Tokens are issued when the `openid` scope is requested. They are JSON Web Tokens (JWT) with three parts: header, payload, and signature, separated by `.` characters.

### JWT Header

| Property | Type | Description |
|----------|------|-------------|
| `typ` | String | Always `JWT` |
| `alg` | String | Signing algorithm: `HS256` or `ES256` |
| `kid` | String | Public key ID. **Only included when `alg` is `ES256`.** |

**HS256 header** (web login):
```json
{"typ": "JWT", "alg": "HS256"}
```

**ES256 header** (native app / LIFF):
```json
{"typ": "JWT", "alg": "ES256", "kid": "a2a459aec5b65fa..."}
```

### Signing Algorithms

| Login Method | Algorithm | Verification Method |
|-------------|-----------|---------------------|
| Web Login (browser redirect) | **HS256** (HMAC-SHA256) | Verify with Channel Secret as symmetric key |
| Native App (LINE SDK) | **ES256** (ECDSA P-256) | Verify with public key from certs endpoint |
| LIFF | **ES256** (ECDSA P-256) | Verify with public key from certs endpoint |

### ES256 Verification

For ES256-signed tokens (native/LIFF):

1. Decode JWT header to get `kid` (Key ID)
2. Fetch public keys: `GET https://api.line.me/oauth2/v2.1/certs`
3. Find the key matching `kid` in the JWK Set response
4. Verify signature using the matched public key

### Claims

| Claim | Type | Description |
|-------|------|-------------|
| `iss` | String | Issuer: `https://access.line.me` |
| `sub` | String | User ID (same as userId in profile) |
| `aud` | String | Channel ID (must match your channel) |
| `exp` | Number | Expiration time (Unix timestamp) |
| `iat` | Number | Issued at (Unix timestamp) |
| `auth_time` | Number | Time of authentication (Unix timestamp). **Only included when `max_age` was sent in authorize request.** |
| `nonce` | String | Nonce value from authorization request (if provided) |
| `amr` | Array | Authentication methods used (see below) |
| `name` | String | Display name (requires `profile` scope) |
| `picture` | String | Profile image URL (requires `profile` scope) |
| `email` | String | Email address (requires `email` scope, user must have verified email) |

### AMR (Authentication Method Reference) Values

| Value | Method |
|-------|--------|
| `pwd` | Email and password |
| `lineautologin` | Auto login |
| `lineqr` | QR code |
| `linesso` | Single Sign-On |
| `mfa` | Multi-factor authentication was performed |

### ID Token Verification Steps

When verifying locally (without using LINE's verify endpoint):

1. Decode JWT header and payload
2. Verify signature (HS256 with Channel Secret, or ES256 with public key)
3. Verify `iss` = `https://access.line.me`
4. Verify `aud` = your Channel ID
5. Verify `exp` > current time
6. Verify `nonce` matches (if sent in authorization request)
7. Optionally verify `auth_time` if `max_age` was specified

## Verify ID Token (Server-side API)

```
POST https://api.line.me/oauth2/v2.1/verify
Content-Type: application/x-www-form-urlencoded
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `id_token` | Yes | Raw ID Token string |
| `client_id` | Yes | Channel ID |
| `nonce` | No | Expected nonce value (validates against token's nonce claim) |
| `user_id` | No | Expected user ID (validates against token's sub claim) |

### Response (200)
```json
{
  "iss": "https://access.line.me",
  "sub": "U1234567890abcdef",
  "aud": "1234567890",
  "exp": 1504169092,
  "iat": 1504263657,
  "nonce": "abc123",
  "amr": ["pwd", "mfa"],
  "name": "LINE User",
  "picture": "https://...",
  "email": "user@example.com"
}
```

**Note**: Using this endpoint is simpler than local verification but adds a network round-trip. For high-throughput scenarios, consider local verification.

## Get UserInfo (OpenID Connect)

```
GET https://api.line.me/oauth2/v2.1/userinfo
Authorization: Bearer {access_token}
```

Also supports `POST`. Requires `openid` scope. Only returns main profile (not subprofile).

### Response (200)
```json
{
  "sub": "U1234567890abcdef",
  "name": "Taro Line",
  "picture": "https://profile.line-scdn.net/..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sub` | String | User ID |
| `name` | String | Display name. Requires `profile` scope. |
| `picture` | String | Profile image URL. Requires `profile` scope. |

**Note**: This is the OpenID Connect UserInfo endpoint. Unlike [Get User Profile](user-profile.md), it requires `openid` scope (not `profile`) and does not return `statusMessage`.

For status codes, response headers, and rate limits, see [api-common.md](api-common.md).
