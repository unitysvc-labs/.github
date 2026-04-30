# UnitySVC Labs

Service-provider catalog repos for the [UnitySVC](https://github.com/unitysvc) platform.

Each `unitysvc-services-*` repo holds the seller-side data (offerings, listings,
upstream access config, code examples, connectivity tests) for one provider.
Tracking issues for each provider live in
[`unitysvc-labs/unitysvc-labs/issues`](https://github.com/unitysvc-labs/unitysvc-labs/issues),
where status / type / reselling labels capture the operational state.

## Provider Catalog

The table below auto-syncs every six hours from the issue-tracker labels and
the per-repo CI runs.  See [`.github/workflows/sync-dashboard.yml`](https://github.com/unitysvc-labs/.github/blob/main/.github/workflows/sync-dashboard.yml).
Private (in-development) providers are tracked but not listed here.

<!-- providers-start -->
| Provider | Repo | Status | Type | Reselling | Active | Validate | Open PRs |
|---|---|---|---|---|---|---|---|
| [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | — | llm | allowed | 3 | ✅ | — |
| [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | — | — | — | — | ✅ | — |
| [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | — | — | — | 1 | ✅ | — |
| [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | — | — | — | — | ❌ | — |
| [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | 🟡 pending-review | — | — | — | ❌ | — |
| [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | — | — | — | 2 | ✅ | — |
| [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | — | llm, image | allowed | 2 | ✅ | — |
| [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | 🔴 rejected | llm | not-allowed | 10 | ✅ | 1 |
| [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | — | — | — | — | ✅ | 1 |
| [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | — | — | — | 3 | ✅ | — |
| [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | — | — | — | 38 | ✅ | 1 |
| [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | 🟡 pending-review | — | — | — | ✅ | 1 |
| [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | — | — | — | — | ✅ | — |
| [Recurrent](https://github.com/unitysvc-labs/unitysvc-labs/issues/35) | [`unitysvc-services-recurrent`](https://github.com/unitysvc-labs/unitysvc-services-recurrent) | — | — | — | — | — | — |
| [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | — | — | — | — | ✅ | — |
| [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | — | — | — | — | ✅ | 1 |
| [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | — | — | — | — | ✅ | — |
| [Template](https://github.com/unitysvc-labs/unitysvc-labs/issues/39) | [`unitysvc-services-template`](https://github.com/unitysvc-labs/unitysvc-services-template) | — | — | — | — | ✅ | — |
<!-- providers-end -->

_Last synced: 2026-04-30 15:39 UTC_

### Column legend

- **Status** — pulled from the tracking issue's `status: …` label.
  🟢 finalized · 🔵 negotiating / discussion · 🟡 pending / awaiting-response ·
  🟠 legal-review · ⚪ on-hold · 🔴 rejected
- **Type** — `type: …` labels (`llm`, `embedding`, `image`, `audio`, `video`, `multimodal`)
- **Reselling** — `reselling: …` label
- **Active** — count of services in `active` status, queried from the gateway via
  `usvc_seller services list --provider <name> --status active`
- **Validate** — most recent CI run conclusion on `main` (✅ success · ❌ failure ·
  🟡 in-progress · ⚪ no-runs / cancelled)
- **Open PRs** — open pull requests on the repo (auto-update PRs from
  `populate-services.yml` count too — that's the signal a refresh is waiting)

## Adding a new provider

1. Create the data repo as `unitysvc-labs/unitysvc-services-<name>` (use the
   [`unitysvc-services-template`](https://github.com/unitysvc-labs/unitysvc-services-template)
   layout).
2. Open a tracking issue in
   [`unitysvc-labs/unitysvc-labs`](https://github.com/unitysvc-labs/unitysvc-labs/issues/new)
   with the provider's display name as the title.  Include
   `Repo: [\`unitysvc-services-<name>\`](https://github.com/unitysvc-labs/unitysvc-services-<name>)`
   in the body so the dashboard sync can map issue → repo.
3. Apply at least one `status: …` label.  The next dashboard sync (or a
   `workflow_dispatch` of `sync-dashboard.yml`) picks it up.
