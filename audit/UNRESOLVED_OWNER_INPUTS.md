# Unresolved Owner Inputs

Only items that genuinely need Andrew’s confirmation before public publication or Play Console finalisation.

## Public identity and contact

| ID | Question | Why needed | Suggested format |
|---|---|---|---|
| O1 | Public developer / legal / trading name | Privacy Policy operator, Terms, footer, Play Console | Exact public string |
| O2 | Public support email | Support, deletion mailto, Privacy contact, Play Console | Address you monitor |
| O3 | Country / business address requirements | Some storefronts/laws need an address | AU address or “email only” decision |
| O4 | GitHub username for Pages | Deployment URLs | e.g. replace `GITHUB_USERNAME` |
| O5 | Governing law / venue | Terms §16 | e.g. Queensland, Australia |

## Audience and product posture

| ID | Question | Why needed |
|---|---|---|
| O6 | Minimum age / target audience | Privacy §16, Play age groups, Families |
| O7 | Is the app directed to children? | Play Families / Declared audience |
| O8 | App vs Game category confirmation | Store listing (recommendation: App) |

## Launch feature flags

| ID | Question | Source evidence |
|---|---|---|
| O9 | Are subscriptions enabled at launch? | No Play Billing dependency found |
| O10 | Is advertising enabled at launch? | No ads SDK found |
| O11 | Will analytics / crash reporting be enabled? | No Firebase/Sentry in audit; diagnostics are local/optional |
| O12 | Will eBay sold-comps be live at launch? | Mobile `isConfigured == false` |
| O13 | Will PokeWallet / pricing backend be live? | Config-gated |
| O14 | Final Android `applicationId` confirmation | Intended `com.cardscanr.app`; code still `com.example.card_scanner_app` |

## Retention and deletion operations

| ID | Question | Why needed |
|---|---|---|
| O15 | Retention periods for cloud profiles, cards, scan sessions, backups, logs | Not encoded in app |
| O16 | Account-deletion SLA / timeframe to publish | Play Data Safety + deletion page |
| O17 | What exactly ops will delete in Supabase Auth + tables | Align deletion page with runbook |
| O18 | Whether local_image_path / OCR text should be excluded from sync | Policy risk |
| O19 | Supabase project region(s) | International transfers wording |
| O20 | Support response-time target | Support page |

## Policy publication dates

| ID | Question |
|---|---|
| O21 | Privacy Policy effective date |
| O22 | Approval that public HTML may drop `OWNER_ACTION_REQUIRED` tokens |

## Notes

- GitHub remote org `Motiv8ed` was observed on the app repository remote URL; **do not assume** this is the public legal name without O1.
- Do not invent a support address. Prefill mailto only after O2.
