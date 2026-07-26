# Permissions and SDK Audit — CardScanR

**Source:** `D:\Card Scanner App` @ `bcb22f613d2301cccacd05f1bf3079d50ff737f8`

## Android permissions (app manifest)

Declared in `card_scanner_app/android/app/src/main/AndroidManifest.xml`:

| Permission | Why it exists | Core functionality? | Notes |
|---|---|---|---|
| `CAMERA` | Live and still card scanning | Yes | Requested when scanning (PrivacyTrustScreen) |
| `INTERNET` | Auth, sync, catalogue, pricing, artwork | Yes | Required for signed-in and online features |

### Not declared in app manifest (but relevant)

| Topic | Finding |
|---|---|
| `READ_MEDIA_IMAGES` / storage | Not in app manifest. Gallery access uses `image_picker` (system photo picker / plugin). Confirm merged manifest from plugins before Play declaration. |
| Location | Not declared |
| Notifications | No FCM/notification permission found in audit |
| Microphone | Not declared |

**Action:** Before AAB upload, run `./gradlew :app:processReleaseManifest` (or equivalent) and re-check the **merged** manifest for plugin-added permissions. Flag any unexpected additions in Play Console declarations.

## Application ID

| Item | Value | Status |
|---|---|---|
| Intended Play package | `com.cardscanr.app` | Owner target |
| Audited `applicationId` / namespace | `com.example.card_scanner_app` | **Must change** before production |
| Debug suffix | `.qa` | QA builds |
| Internal beta suffix | `.beta` when `cardscanrInternalBeta=true` | Optional channel |

## Flutter / Dart dependency inventory (production-relevant)

From `pubspec.yaml` (direct dependencies):

| Package | Role | Data sensitivity |
|---|---|---|
| `camera` | Capture | Camera frames |
| `image_picker` | Gallery/camera stills | Photos |
| `google_mlkit_text_recognition` | On-device OCR | Local image→text |
| `supabase_flutter` | Auth + DB | Account + sync |
| `http` | API calls | Query payloads |
| `sqflite` / `sqlite3_flutter_libs` | Local DB | Collection |
| `shared_preferences` | Settings | Preferences |
| `path_provider` | Local files | Caches/exports |
| `cached_network_image` | Artwork cache | Catalogue images |
| `share_plus` / `flutter_file_dialog` | Share/export files | User-initiated |
| `url_launcher` | Open links | None by itself |
| `archive` / `crypto` / `uuid` / `image` | Utilities | Local |
| `flutter_svg` | Brand SVG | None |
| `cupertino_icons` | Icons | None |

### Not present in audited `pubspec.yaml`

- Firebase / Analytics / Crashlytics  
- Sentry  
- AdMob or other ad SDKs  
- `in_app_purchase` / Play Billing  
- `google_sign_in` package (Google sign-in is via Supabase OAuth browser/custom tab flow)  
- Push notification SDKs  

## Native Android dependencies (`build.gradle.kts`)

| Dependency | Role |
|---|---|
| `org.opencv:opencv:4.9.0` | Computer vision / card geometry helpers |
| `com.google.mlkit:text-recognition:16.0.1` | Latin OCR |
| `com.google.mlkit:text-recognition-japanese:16.0.1` | Japanese OCR |

## Potential undeclared collection

| Risk | Detail | Severity |
|---|---|---|
| `local_image_path` synced to Supabase | String field on `user_cards`; may store storage location or path-like strings | Medium — clarify semantics; avoid syncing absolute device paths if not needed |
| `raw_ocr_text` on `scan_sessions` | OCR text uploaded when sessions are cloud-saved | Medium — disclose in privacy/Data Safety |
| Diagnostics exports | May include scan evidence if user shares | Low if user-initiated only |
| Third-party API query logs | Providers may log card queries / IPs | Medium — disclose processors |
| Plugin merged permissions | image_picker/camera/share may add permissions | Medium — verify merged manifest |
| Release signing still debug | `signingConfig = debug` in release | High for store readiness (not privacy, but release hygiene) |

## Unnecessary permissions requiring removal

None identified in the **app-authored** manifest beyond CAMERA + INTERNET. Re-check after merged manifest review. Do not add advertising or precise location permissions without a product need.

## Deep link

`cardscanr://login-callback` intent-filter for Supabase OAuth PKCE redirect.
