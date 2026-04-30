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
| Provider | Repo | Type | Lifecycle | Visibility | Listing type | Status | Open PRs |
|---|---|---|---|---|---|---|---|
| [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 3 active · 3 rejected revisions | 3 published | 3 regular | 🟡 | — |
| [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 8 rejected | 8 unlisted | 8 byok | 🔴 | — |
| [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 1 active · 3 rejected · 1 rejected revision | 1 published · 3 unlisted | 4 byok | 🟡 | — |
| [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 13 rejected | 13 unlisted | 13 byok | 🔴 | — |
| [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | — | — | — | — | 🔴 | — |
| [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | — | — | — | — | ⚪ | — |
| [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | image_generation, llm | 2 active · 4 rejected · 2 rejected revisions | 2 published · 4 unlisted | 6 regular | 🟡 | — |
| [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 10 active · 6 rejected · 10 rejected revisions | 10 published · 6 unlisted | 16 byok | 🟡 | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 1 deprecated · 111 rejected | 112 unlisted | 112 byok | 🔴 | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 3 active · 1 rejected · 3 rejected revisions | 3 published · 1 unlisted | 4 byok | 🟡 | — |
| [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 36 active · 15 rejected · 36 rejected revisions | 36 published · 15 unlisted | 51 byok | 🟡 | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 28 rejected | 28 unlisted | 28 byok | 🔴 | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | — | — | — | — | ⚪ | — |
| [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | — | — | — | — | 🟡 | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 36 active · 24 rejected · 36 rejected revisions | 36 published · 24 unlisted | 60 regular | 🟡 | — |
| [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | content | 6 active · 2 rejected | 6 published · 2 unlisted | 5 regular · 3 byok | 🟡 | — |
| [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 7 rejected | 7 unlisted | 7 byok | 🔴 | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | email | 3 rejected | 3 unlisted | 1 regular · 2 byok | 🔴 | — |
| [Template](https://github.com/unitysvc-labs/unitysvc-labs/issues/39) | [`unitysvc-services-template`](https://github.com/unitysvc-labs/unitysvc-services-template) | content, email, llm, proxy | 13 active · 2 rejected | 13 published · 2 unlisted | 8 regular · 6 byok · 1 byoe | 🟡 | — |
| **Total** (19 repos) | — | — | 110 active · 1 deprecated · 227 rejected · 91 rejected revisions | 110 published · 228 unlisted | 83 regular · 254 byok · 1 byoe | — | 6 |
<!-- providers-end -->

_Last synced: 2026-04-30 19:19 UTC_

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
