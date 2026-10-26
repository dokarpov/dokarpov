# Portfolio measurement — evidence before optics

**Goal:** distinguish attention to a GitHub repository from interest in a product, actual usage, and customer value. All numbers must have a source, denominator, observation window and collection method.

## Measurement layers

| Layer | Primary source | Useful measure | It cannot establish |
| --- | --- | --- | --- |
| GitHub discovery | GitHub Traffic API | Repository views, unique visitors, clones, top referrers and paths | Whether a visitor is a recruiter or has evaluated the product |
| Public portfolio / demos | Cloudflare Web Analytics (once configured) | Pages visited, traffic sources and page performance | Sign-ups or qualified demand without explicit conversion events |
| Product activation | Instrumented first-party application events | Completed first-value journey, eligible sessions, time-to-value | Satisfaction or retention from page views alone |
| Business validation | Verified consented pilot and billing data | Activated merchants/users, repeat usage, paid conversions, costs | Causality without a controlled design |

## GitHub Traffic API snapshot

The repository includes a **scheduled snapshot workflow** and a Python collector. The job is **disabled until credentials are configured**; no existing historic dataset is claimed.

Activation requires:

1. Create a **fine-grained GitHub token** scoped to the selected public repositories with **Administration: Read** only. The GitHub traffic endpoints require this permission; avoid general-purpose broad personal access tokens.
2. Set the repository Actions secret `PORTFOLIO_TRAFFIC_TOKEN`.
3. Set the repository Actions variable `ENABLE_TRAFFIC_SNAPSHOT` to `true`.
4. Run **Actions → GitHub traffic snapshot → Run workflow**, then verify that an artifact was produced and its collected_at time is recent.

The workflow saves JSON snapshots as **GitHub Actions artifacts** (retention: 90 days, subject to repository settings). Artifacts in a public repository may be accessible according to GitHub's Actions permissions; store sensitive analysis in a separate private system. The workflow does **not** commit counts into this public profile. A permanent historic warehouse should be a separate private repository or database if needed later.

API values are limited to a rolling **14-day window** and top referrers/paths are capped. **Do not sum overlapping 14-day unique-visitor totals** into a monthly unique count. For daily views, prefer date-keyed observations; identify revisions when a newer snapshot supersedes a previous count. Bot filtering and attribution are imperfect.

## Website analytics next

For GitHub Pages websites, create a Cloudflare Web Analytics site/property and insert the **site-specific official beacon** in the published HTML after obtaining its real token. Do not commit placeholder tokens and claim tracking is enabled. Record source campaign parameters for links in CV and LinkedIn, and use explicitly defined events for `demo_opened`, `core_flow_completed`, `contact_intent` where supported by the chosen analytics provider.

Do not send CVs, names, email addresses, financial records or customer identifiers in telemetry payloads. Evaluate EU data-protection requirements and provide an accurate privacy notice before collecting website or application events.

## Product evidence gates

- **Attention:** real collected GitHub or web page views, dated.
- **Engagement:** an observed interaction with a published experience.
- **Activation:** user completes the documented first-value job.
- **Retention:** repeat behavior by a pseudonymous, consent-compliant cohort, on a defined window.
- **Business value:** verified willing-to-pay, revenue and service economics.

CI test passes, AI-generated documentation, simulated users and mock fixtures belong to **engineering evidence**, never customer adoption or commercial traction.
