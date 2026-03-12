# LINE URL Schemes

Deep links to LINE app screens. Use in URI actions (Flex Message, Template, Rich Menu, Quick Reply).

**Platform:** iOS and Android only. Not supported on LINE desktop (macOS/Windows).

**Prefix:** Use `https://line.me/R/` (preferred). The `line://` scheme is **deprecated** (no removal date set, but avoid for new development).

**Behavior:** If LINE is installed, opens the corresponding screen. If not installed, `https://line.me/R/` redirects to the download page; `line://` does nothing.

## Official Account

| Action | URL |
|--------|-----|
| Open OA profile/chat | `https://line.me/R/ti/p/{percent-encoded LINE ID}` |
| Share OA with contacts | `https://line.me/R/nv/recommendOA/{percent-encoded LINE ID}` |
| Open OA chat | `https://line.me/R/oaMessage/{percent-encoded LINE ID}` |
| Open OA chat with pre-filled text | `https://line.me/R/oaMessage/{percent-encoded LINE ID}/?{text}` |

LINE ID must be percent-encoded (UTF-8), including the `@` prefix (e.g., `%40linedevelopers`).

## Sharing

| Action | URL |
|--------|-----|
| Share text to contacts | `https://line.me/R/share?text={percent-encoded text}` |

## LINE VOOM

| Action | URL |
|--------|-----|
| OA's VOOM timeline | `https://line.me/R/home/public/main?id={ID without @}` |
| OA's business profile | `https://line.me/R/home/public/profile?id={ID without @}` |
| Specific VOOM post | `https://line.me/R/home/public/post?id={ID without @}&postId={postId}` |

Note: `id` parameter does **not** include the `@` prefix.

## LINE App Screens

| Action | URL |
|--------|-----|
| Chat tab | `https://line.me/R/nv/chat` |
| Shopping tab | `https://line.me/R/nv/commerce` |
| Wallet tab | `https://line.me/R/nv/wallet` |
| Add friends | `https://line.me/R/nv/addFriends` |
| Official accounts directory | `https://line.me/R/nv/officialAccounts` |
| LINE VOOM (following) | `https://line.me/R/nv/timeline` |
| My profile | `https://line.me/R/nv/profile` |
| Set LINE ID | `https://line.me/R/nv/profileSetId` |

## Settings

| Action | URL |
|--------|-----|
| Settings | `https://line.me/R/nv/settings` |
| Account | `https://line.me/R/nv/settings/account` |
| Authorized apps | `https://line.me/R/nv/connectedApps` |
| Connected devices | `https://line.me/R/nv/connectedDevices` |
| Privacy | `https://line.me/R/nv/settings/privacy` |
| Stickers | `https://line.me/R/nv/settings/sticker` |
| My Stickers | `https://line.me/R/nv/stickerShop/mySticker` |
| Themes (iOS) | `https://line.me/R/nv/settings/themeSettingsMenu` |
| Themes (Android) | `https://line.me/R/nv/settings/theme` |
| My Themes | `https://line.me/R/nv/themeSettings` |
| Notification > Authorized apps | `https://line.me/R/nv/notificationServiceDetail` |
| Chats | `https://line.me/R/nv/settings/chatSettings` |
| Display suggestions | `https://line.me/R/nv/suggestSettings` |
| Calls | `https://line.me/R/nv/settings/callSettings` |
| Friends | `https://line.me/R/nv/settings/addressBookSync` |
| LINE VOOM | `https://line.me/R/nv/settings/timelineSettings` |

## Camera / Media

| Action | URL |
|--------|-----|
| Open camera | `https://line.me/R/nv/camera/` |
| Select single image | `https://line.me/R/nv/cameraRoll/single` |
| Select multiple images | `https://line.me/R/nv/cameraRoll/multi` |
| Select location | `https://line.me/R/nv/location/` |

Camera/media schemes only work from LINE chat (including OpenChat). Not available in LIFF apps or external apps.

Location scheme only works in one-on-one chats between user and LINE Official Account.

## Sticker / Theme Shop

| Action | URL |
|--------|-----|
| Sticker detail | `https://line.me/R/shop/sticker/detail/{package_id}` |
| Sticker category ranking | `https://line.me/R/shop/category/{category_id}` |
| Creator's sticker collection | `https://line.me/R/shop/sticker/author/{author_id}` |
| Sticker Shop HOME | `https://line.me/R/nv/stickerShop` |
| Sticker Shop RANK | `https://line.me/R/shop/sticker/hot` |
| Sticker Shop NEW | `https://line.me/R/shop/sticker/new` |
| Sticker Shop FREE | `https://line.me/R/shop/sticker/event` |
| Sticker Shop CATEGORIES | `https://line.me/R/shop/sticker/category` |
| Theme detail | `https://line.me/R/shop/theme/detail?id={product_id}` |

## LIFF / LINE MINI App

| Action | URL |
|--------|-----|
| Open LIFF app | `https://liff.line.me/{liffId}` |
| LIFF with path and query | `https://liff.line.me/{liffId}/path?key=value` |
| Open LINE MINI App | `https://miniapp.line.me/{miniAppId}` |

Deprecated LIFF formats: `https://line.me/R/app/{liffId}` and `line://app/{liffId}`.

## Browser Control Parameters

Append to `https://` URLs in URI actions:

| Parameter | Effect |
|-----------|--------|
| `?openExternalBrowser=1` | Force open in external browser instead of LINE's in-app browser |
| `?openInAppBrowser=0` | Use Chrome Custom Tab instead of in-app browser (**Android only**) |

These parameters do **not** work with LIFF apps.
