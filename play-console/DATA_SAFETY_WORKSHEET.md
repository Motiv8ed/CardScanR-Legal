# Google Play Data Safety Worksheet — CardScanR

**Draft only.** Complete final answers after owner inputs and any app changes.  
**Evidence HEAD:** `bcb22f613d2301cccacd05f1bf3079d50ff737f8`  
**Confidence:** High = source-confirmed; Medium = needs nuance; Low = owner/product confirmation.

## Global questions

| Play question | Draft answer | Evidence | Confidence |
|---|---|---|---|
| Does the app collect or share user data? | **Yes — collects.** Sharing limited to service providers / APIs needed for functionality (not “sold”). | Supabase auth/sync; HTTPS catalogue/pricing | High |
| Is all user data encrypted in transit? | **Yes** for network calls (HTTPS / Supabase TLS). | `http`/`supabase_flutter` over HTTPS | High |
| Do users can request data deletion? | **Yes externally** via published deletion URL/email once contact confirmed. **In-app deletion: No** today. | PrivacyTrustScreen; AccountScreen sign-out only | High |
| Account deletion available? | Declare **deletion request supported** via web/email; note in-app not yet available until implemented. Play requires a URL — use delete-account page. | Same | High |
| Independent security review? | **No** (unless owner commissions one) | — | Low |

## Data types — collection & sharing

For each type: Collected? Shared? Ephemeral? Required? Purpose.

### Personal info — Name

| Field | Draft |
|---|---|
| Collected? | Yes (display name / Google full_name metadata) |
| Shared? | With Supabase as processor; not sold |
| Processing ephemeral? | No |
| Required? | Optional/collected as available from auth/onboarding |
| Purposes | App functionality, Account management |
| Evidence | `UserProfile`, AccountScreen |
| Confidence | High |

### Personal info — Email address

| Field | Draft |
|---|---|
| Collected? | Yes |
| Shared? | Supabase Auth; Google if Google sign-in |
| Ephemeral? | No |
| Required? | Required for email auth accounts; obtained for Google accounts |
| Purposes | App functionality, Account management |
| Confidence | High |

### Personal info — User IDs

| Field | Draft |
|---|---|
| Collected? | Yes (Supabase user UUID) |
| Shared? | Stored in Supabase; used as FK on user tables |
| Ephemeral? | No |
| Required? | Yes for signed-in cloud features |
| Purposes | App functionality, Account management |
| Confidence | High |

### Personal info — Address

| Field | Draft |
|---|---|
| Collected? | Country code only (not street address) |
| Recommendation | Prefer **Other info** / avoid full Address type unless Play forces country under Address |
| Confidence | Medium |

### Photos and videos

| Field | Draft |
|---|---|
| Collected? | Yes — camera/gallery for scanning |
| Shared? | Not as a dedicated photo upload API in audit; Cloud Vision stub inactive. Metadata sync may include catalogue `image_url` and `local_image_path` strings. Diagnostics may include scan evidence if user exports/shares. |
| Ephemeral? | **Do not select ephemeral-only** until QA proves still images are discarded. Live preview frames may be transient; still captures/files may remain locally. |
| Required? | Optional to deny camera (manual entry available per in-app copy); gallery optional |
| Purposes | App functionality |
| Confidence | Medium (collection High; ephemeral Low) |

### App activity — In-app search / scan activity

| Field | Draft |
|---|---|
| Collected? | Yes — scan sessions, OCR text, queries to catalogue APIs |
| Shared? | Catalogue/pricing providers receive query parameters; Supabase stores sessions |
| Purposes | App functionality |
| Confidence | High |

### App activity — Other user-generated content (collection)

| Field | Draft |
|---|---|
| Collected? | Yes — inventory, notes, binders/goals locally; cloud sync when signed in |
| Shared? | Supabase when synced |
| Purposes | App functionality |
| Confidence | High |

### Financial info

| Field | Draft |
|---|---|
| Play Billing purchases? | **No** in audited deps |
| User-entered card purchase prices? | Yes, as collection fields |
| Recommendation | If Play has no perfect fit, use **Other financial info** only if required; otherwise describe under app activity. Confirm with O9. |
| Confidence | Medium |

### Device or other IDs

| Field | Draft |
|---|---|
| Advertising ID? | **No** evidence |
| Other IDs? | App/user IDs as above |
| Confidence | High for ads ID absence |

### App info and performance — Crash logs / Diagnostics

| Field | Draft |
|---|---|
| Collected automatically? | **No** Crashlytics/Sentry in audit |
| Optional diagnostics? | Yes, user/dev initiated exports |
| Declare? | Usually **No** automatic collection unless O11 enables SDK |
| Confidence | High current; Low if launch plan adds SDK |

### Location

| Field | Draft |
|---|---|
| Collected? | **No** device location permission |
| Confidence | High |

### Web browsing / contacts / SMS / health

| Field | Draft |
|---|---|
| Collected? | **No** evidence |
| Confidence | High |

## Purposes checklist (map carefully in Console)

- App functionality: Yes  
- Analytics: No (current) / O11  
- Developer communications: Support email only if user contacts you  
- Advertising/marketing: No (current) / O10  
- Fraud prevention: Only if later added  
- Personalisation: Limited (profile market prefs)  
- Account management: Yes  

## Required vs optional

| Data | Required for basic use? |
|---|---|
| Camera | Optional (manual entry available) but core for scanner UX |
| Account | Required for cloud sync; confirm whether guest/local-only mode is supported for reviewers |
| Collection data | Core when user saves cards |

## Encryption

| At rest | In transit |
|---|---|
| OS/device storage protections; no app-level encryption claim found | HTTPS — Yes |

## Data deletion / account deletion form fields

| Console field | Draft |
|---|---|
| URL for account deletion | `https://motiv8ed.github.io/CardScanR-Legal/delete-account/` |
| Also acceptable alias | `https://motiv8ed.github.io/CardScanR-Legal/data-deletion/` (canonical: delete-account) |
| In-app deletion | Not available — implement before relying on in-app path (see APP_CHANGES_REQUIRED) |

## Sharing definition caution

Play distinguishes “sharing” with third parties. Service providers acting on your behalf may be excluded under certain Console definitions if disclosed as processors — **follow the Console’s current wording** and list APIs that operate as independent controllers (Google sign-in, TCGdex, Pokémon TCG API, etc.) accurately.
