# LIFF CLI

CLI tool for LIFF app management and local development.

- **npm**: `@line/liff-cli`
- **GitHub**: [line/liff-cli](https://github.com/line/liff-cli)
- **Install**: `npm install -g @line/liff-cli`

---

## 1. Channel Management

Register channels before using other commands.

```bash
# Add a channel (prompts for channel secret)
liff-cli channel add 1234567890

# Set default channel (used when --channel-id is omitted)
liff-cli channel use 1234567890
```

---

## 2. LIFF App CRUD

Mirrors the [Server API](server-api.md) but from the command line.

### Create

```bash
liff-cli app create \
  --channel-id 1234567890 \
  --name "My App" \
  --endpoint-url https://example.com \
  --view-type full
# → Successfully created LIFF app: 1234567890-AbcdEfgh
```

| Option | Required | Description |
|--------|:---:|-------------|
| `-c`, `--channel-id` | | Channel ID (default channel if omitted) |
| `-n`, `--name` | Yes | App name (cannot contain "LINE") |
| `-e`, `--endpoint-url` | Yes | HTTPS URL, no fragments |
| `-v`, `--view-type` | Yes | `full`, `tall`, or `compact` |

### Update

```bash
liff-cli app update --liff-id 1234567890-AbcdEfgh --name "New Name"
```

Same options as create, all optional except `--liff-id` (required).

### List

```bash
liff-cli app list --channel-id 1234567890
```

### Delete

```bash
liff-cli app delete --liff-id 1234567890-AbcdEfgh
```

---

## 3. Quick Setup (`init`)

One command to: add channel → create LIFF app → scaffold project template.

```bash
liff-cli init \
  --channel-id 1234567890 \
  --name "My App" \
  --view-type full \
  --endpoint-url https://example.com
```

Omit options for interactive prompts. Internally runs [Create LIFF App](https://www.npmjs.com/package/@line/create-liff-app) for scaffolding (React/Vue/Svelte/Next.js/Nuxt/vanilla, JS/TS).

---

## 4. Scaffold Only

Create a project template without channel/app setup:

```bash
liff-cli scaffold my-app --liff-id 1234567890-AbcdEfgh
```

---

## 5. Local HTTPS Dev Server (`serve`)

Launch a local proxy server with HTTPS and auto-update the endpoint URL.

```bash
liff-cli serve \
  --liff-id 1234567890-AbcdEfgh \
  --url http://localhost:3000/

# → LIFF URL:     https://liff.line.me/1234567890-AbcdEfgh
# → Proxy server: https://localhost:9000/
```

**WARNING**: The `serve` command **rewrites the endpoint URL** to your local proxy. Do NOT run this on a published LIFF app — users will lose access.

### Prerequisites: SSL Certificates

The `serve` command requires valid certificates for localhost. Use [mkcert](https://github.com/FiloSottile/mkcert):

```bash
# Install mkcert
brew install mkcert          # macOS
choco install mkcert         # Windows

# Create local CA + certificates
mkcert -install
mkcert localhost
# → localhost.pem + localhost-key.pem
```

Run the `serve` command from the directory containing these certificate files.

### LIFF Inspector (Debug on Mobile)

Add `--inspect` to launch LIFF Inspector Server — debug your LIFF app on mobile with Chrome DevTools on PC:

```bash
liff-cli serve \
  --liff-id 1234567890-AbcdEfgh \
  --url http://localhost:3000/ \
  --inspect

# Terminal outputs a devtools:// URL → open in Chrome to debug
```

Requires [@line/liff-inspector](https://www.npmjs.com/package/@line/liff-inspector) plugin installed in your LIFF app.

### Expose via ngrok

Use `--proxy-type ngrok` to expose your local server publicly (requires [ngrok](https://ngrok.com/) account):

```bash
NGROK_AUTHTOKEN={token} liff-cli serve \
  --liff-id 1234567890-AbcdEfgh \
  --url http://localhost:3000/ \
  --proxy-type ngrok

# → Proxy server: https://1234abcd.ngrok.example.com/
```

### Serve Options

| Option | Required | Description |
|--------|:---:|-------------|
| `-l`, `--liff-id` | Yes | LIFF ID (must be in default channel) |
| `-u`, `--url` | * | Local dev server URL |
| `--host` | * | Local dev server host |
| `--port` | * | Local dev server port |
| `-i`, `--inspect` | | Launch LIFF Inspector |
| `--proxy-type` | | `local-proxy` (default), `ngrok`, or `ngrok-v1` (deprecated) |
| `--local-proxy-port` | | Proxy listen port (default: 9000) |

\* Either `--url` or `--host` + `--port` is required.

---

## Typical Development Workflow

```
1. liff-cli init (or channel add + app create + scaffold separately)
2. cd my-app && npm run dev          ← start local dev server
3. mkcert localhost                  ← create SSL certs (once)
4. liff-cli serve -l {liffId} -u http://localhost:3000/
5. Open LIFF URL on phone to test
6. (Optional) Add --inspect for Chrome DevTools debugging
```
