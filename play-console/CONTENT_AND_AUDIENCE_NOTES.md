# Content and Audience Notes — CardScanR

Evidence-based recommendations for Play Console questionnaires. Not legal advice.

## App versus game

| Recommendation | **App** (not Game) |
|---|---|
| Evidence | Utility for scanning/collecting TCG cards; no game loop / scores as primary purpose |

## Ads declaration

| Recommendation | **No ads** for current audited source |
|---|---|
| Evidence | No AdMob/ads SDK in `pubspec.yaml` |
| Owner check | O10 — if ads added later, redeclare |

## Target age groups

| Recommendation | Draft **18+** or **older teens and adults** until O6/O7 confirmed |
|---|---|
| Caution | Pokémon IP appeals to children; if not designing for children, say so clearly and avoid Families policy unless compliant |
| Owner check | O6, O7 |

## Children / Families

| Recommendation | Do **not** enrol in Designed for Families unless product, content, and ads (none) fully meet policy and O7 says yes |
|---|---|
| Evidence | Auth, camera, cloud sync, market estimates — typically not a child-directed setup without extra work |

## Content rating (IARC / questionnaire hints)

| Topic | Likely answer direction |
|---|---|
| Violence | None |
| Sexual content | None |
| Language | None expected |
| Controlled substances | None |
| User interaction | Users may sync personal collections; UGC is card photos/notes — limited social features not observed as a public feed |
| Share location | No |
| Digital purchases | None in audit (O9) |

Complete the official questionnaire honestly; do not copy these as final without walking the form.

## Financial-feature considerations

- No Play Billing in audit  
- Shows **estimate** market values and user-entered purchase prices  
- Disclose that values are not financial advice or brokerage  

## User-generated-content considerations

- Users capture card images and may enter notes  
- No public social feed identified in audit  
- If Play asks about UGC, describe private collection content + optional support diagnostics  

## Permissions declarations

| Permission | Declare |
|---|---|
| Camera | Yes — card scanning |
| Internet / network | Yes — account, sync, catalogue, pricing |
| Photos/media | Only if merged manifest or photo picker declaration requires it — verify |
| Notifications | No evidence |
| Location | No |

## Privacy policy / deletion URLs

Must be live HTTPS Pages URLs before Data Safety submission.
