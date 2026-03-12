# Channel Access Token Management

Issue, verify, and revoke channel access tokens required for calling the Messaging API.

## Token Types

| Type | Lifetime | Max per channel | Issuance method | Recommended use |
|------|----------|-----------------|-----------------|-----------------|
| Long-lived | No expiration (manual) | — | LINE Developers Console | Development/testing only |
| Short-lived | 30 days | 30 (oldest auto-revoked) | client_id + client_secret | Simple production |
| v2.1 | Custom (up to 30 days) | 30 | JWT assertion | Production (recommended) |
| Stateless | ~15 minutes | No limit | client_id/secret OR JWT | Serverless, high-security |

Expired tokens are not counted toward the per-channel limit.

## Channel Access Token v2.1 (Recommended)

Issues tokens with a custom expiration using JWT assertion for authentication.

### Assertion Signing Key Setup

1. Generate RSA key pair: **RSA 2048-bit minimum**, JWK (RFC 7517) format, `alg: RS256`, `use: sig`
2. Register **public key** on LINE Developers Console → channel's Basic Settings → "Register a public key"
3. Console returns a `kid` (key ID) — use this in JWT header

**Public key must NOT include `kid` before registration.** The Console assigns it.

```python
# Example: generate key pair with jwcrypto
from jwcrypto import jwk
key = jwk.JWK.generate(kty='RSA', alg='RS256', use='sig', size=2048)
private_key = key.export_private()  # keep secret
public_key = key.export_public()    # register on Console
```

### JWT Structure

The `client_assertion` is a JWT with three parts: header.payload.signature

**Header:**
```json
{"alg": "RS256", "typ": "JWT", "kid": "<kid from Console>"}
```

**Payload (claims):**

| Claim | Value |
|-------|-------|
| `iss` | Channel ID |
| `sub` | Channel ID (same as `iss`) |
| `aud` | `https://api.line.me/` |
| `exp` | JWT expiration — UNIX timestamp, **max 30 minutes** from creation |
| `token_exp` | Access token validity in **seconds** (max 2,592,000 = 30 days) |

**Signature:** Sign with RS256 using the private key.

### Issue

`POST https://api.line.me/oauth2/v2.1/token`

Content-Type: `application/x-www-form-urlencoded`

| Parameter | Value |
|-----------|-------|
| `grant_type` | `client_credentials` |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` |
| `client_assertion` | JWT signed with private key (see above) |

Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 2592000,
  "key_id": "sDTOzw5wIfW..."
}
```

Max 30 tokens per channel. If the limit is reached, additional requests are blocked.

### Verify

`GET https://api.line.me/oauth2/v2.1/verify?access_token={token}`

Response:
```json
{
  "client_id": "1234567890",
  "expires_in": 2591659,
  "scope": "profile chat_message.write"
}
```

- `scope` is not always included

### Get all valid key IDs

`GET https://api.line.me/oauth2/v2.1/tokens/kid`

Query: `client_assertion_type` + `client_assertion` (same as issue)

Response:
```json
{
  "kids": ["sDTOzw5wIfW...", "anotherKeyId..."]
}
```

### Revoke

`POST https://api.line.me/oauth2/v2.1/revoke`

Content-Type: `application/x-www-form-urlencoded`

Body: `client_id={channelId}&client_secret={channelSecret}&access_token={token}`

Returns `200` with empty body. No error occurs if an invalid token is specified.

Revoke when:
- Old tokens are no longer needed after reissue
- A token is suspected to have been leaked
- No need to revoke already-expired tokens

## Stateless Channel Access Token

Issues tokens valid for ~15 minutes only. No limit on the number of tokens. Cannot be revoked once issued.

`POST https://api.line.me/oauth2/v3/token`

Content-Type: `application/x-www-form-urlencoded`

**Method 1: channel ID and channel secret**

| Parameter | Value |
|-----------|-------|
| `grant_type` | `client_credentials` |
| `client_id` | Channel ID |
| `client_secret` | Channel secret |

**Method 2: JWT assertion**

| Parameter | Value |
|-----------|-------|
| `grant_type` | `client_credentials` |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer` |
| `client_assertion` | JWT (same as v2.1) |

Response:
```json
{
  "token_type": "Bearer",
  "access_token": "ey...",
  "expires_in": 900
}
```

## Short-lived Channel Access Token

`POST https://api.line.me/v2/oauth/accessToken`

Content-Type: `application/x-www-form-urlencoded`

Body: `grant_type=client_credentials&client_id={channelId}&client_secret={channelSecret}`

- Validity: 30 days
- Max 30 tokens per channel. If exceeded, the oldest token is automatically revoked
- Tokens cannot be refreshed — issue a new one before expiration
- Rate limit: 370 req/sec

Response:
```json
{
  "access_token": "W1TeHCgfH2Liwa...",
  "expires_in": 2592000,
  "token_type": "Bearer"
}
```

## Verify Short-lived / Long-lived Token

`POST https://api.line.me/v2/oauth/verify`

Content-Type: `application/x-www-form-urlencoded`

Body: `access_token={token}`

Response:
```json
{
  "client_id": "1350031035",
  "expires_in": 3138007490,
  "scope": "P CM"
}
```

- `scope` is not always included

## Revoke Short-lived / Long-lived Token

`POST https://api.line.me/v2/oauth/revoke`

Content-Type: `application/x-www-form-urlencoded`

Body: `access_token={token}`

Returns `200` with empty body. No error occurs if an invalid token is specified.

## Token Rotation Strategy

1. Issue a new token before the current one expires
2. Confirm the new token works, then revoke the old one
3. Multiple valid tokens can coexist
4. Use the v2.1 `kids` endpoint to monitor the number of active tokens
