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
| Provider | Repo | Type | Lifecycle | Visibility | Listing type | Validate | Open PRs |
|---|---|---|---|---|---|---|---|
| [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 3 active · 3 rejected revisions | 3 published | 3 regular | ✅ | — |
| [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 9 rejected | 9 unlisted | 9 byok | ✅ | — |
| [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 1 active · 3 rejected · 1 rejected revision | 1 published · 3 unlisted | 4 byok | ✅ | — |
| [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 20 rejected | 20 unlisted | 20 byok | ❌ | — |
| [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | — | — | — | — | ❌ | — |
| [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 2 active · 2 rejected revisions | 2 published | 2 byok | ✅ | — |
| [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | image_generation, llm | 2 active · 7 rejected · 2 rejected revisions | 2 published · 7 unlisted | 9 regular | ✅ | — |
| [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 10 active · 6 rejected · 10 rejected revisions | 10 published · 6 unlisted | 16 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 1 deprecated · 122 rejected | 123 unlisted | 123 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 3 active · 2 rejected · 3 rejected revisions | 3 published · 2 unlisted | 5 byok | ✅ | — |
| [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 38 active · 22 rejected · 38 rejected revisions | 38 published · 22 unlisted | 60 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 45 deprecated · 31 rejected | 76 unlisted | 46 regular · 30 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | — | — | — | — | ✅ | — |
| [Recurrent](https://github.com/unitysvc-labs/unitysvc-labs/issues/35) | [`unitysvc-services-recurrent`](https://github.com/unitysvc-labs/unitysvc-services-recurrent) | — | — | — | — | — | — |
| [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | — | — | — | — | ✅ | — |
| [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 8 rejected | 8 unlisted | 8 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | — | — | — | — | ✅ | — |
| [Template](https://github.com/unitysvc-labs/unitysvc-labs/issues/39) | [`unitysvc-services-template`](https://github.com/unitysvc-labs/unitysvc-services-template) | — | — | — | — | ✅ | — |
<!-- providers-end -->

_Last synced: 2026-04-30 18:23 UTC_

### Column legend

- **Type** — `type: …` labels on the tracking issue (`llm`, `embedding`,
  `image`, `audio`, `video`, `multimodal`).  Labels are platform-coarse;
  per-service `service_type` lives on each `Service` record.
- **Lifecycle** — service-status counts from the gateway, summed across
  every service the provider owns: `active`, `draft`, `review`,
  `deprecated` (and `pending` / `rejected` / `suspended` when present).
- **Visibility** — catalog-visibility counts: `published` (= `public`)
  and `unlisted`.  Private services are tracked but not shown on this
  public README.
- **Mode** — enrollment-mode counts: `managed` (seller provides upstream
  credentials), `byok` (customer supplies API key), `byoe` (customer
  supplies endpoint + key).  *Currently unpopulated — see
  `fetch_mode_counts` in `scripts/sync_dashboard.py` for the open
  question on how to derive it.*
- **Validate** — most recent CI run conclusion on `main`: ✅ success ·
  ❌ failure · 🟡 in-progress · ⚪ no-runs / cancelled.
- **Open PRs** — open pull requests on the repo.  Auto-update PRs from
  `populate-services.yml` count too — that's the signal a refresh is
  waiting on a human.

## Adding a new provider

1. Create the data repo as `unitysvc-labs/unitysvc-services-<name>` (use the
   [`unitysvc-services-template`](https://github.com/unitysvc-labs/unitysvc-services-template)
   layout).
2. Open a tracking issue in
   [`unitysvc-labs/unitysvc-labs`](https://github.com/unitysvc-labs/unitysvc-labs/issues/new)
   with the provider's display name as the title.  Include
   `Repo: [\`unitysvc-services-<name>\`](https://github.com/unitysvc-labs/unitysvc-services-<name>)`
   in the body so the dashboard sync can map issue → repo.
3. Apply any `type: …` labels (drives the **Type** column).  The next
   dashboard sync (or a
   `workflow_dispatch` of `sync-dashboard.yml`) picks it up.
