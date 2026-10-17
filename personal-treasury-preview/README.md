# Personal Treasury — Git preview

Mobile-first preview for validating the Personal Treasury UX before the Lovable production build.

## Included
- Compact Home targeting 360–390 px mobile widths.
- One primary visual canvas with Atlas / Pulse / Flow modes.
- Atlas regrouping by Role / Currency / Account.
- Pulse period controls: 30d / 90d / 1y.
- Reporting-currency switch and hide-amounts privacy control.
- Compact Available / Burn / Runway row.
- Reconciliation review entry point.
- Unified ledger with type filters.
- Analyze view with position, burn, currency and reconciliation visuals.
- Local CSV/TSV statement analysis preview.
- Accounts overview.
- PWA manifest + service worker for installable hosting.

## Privacy
Only synthetic preview data is committed. Statement files selected in the preview are parsed in the browser and are not uploaded.

## Product rule being tested
The UI treats economic movements, rather than flat bank transactions, as the core model: internal transfers should not inflate spending; original currencies remain meaningful; incomplete coverage stays explicit.

## Branch
This preview intentionally lives on the `personal-treasury-preview` branch and does not modify the profile repository's main branch.
