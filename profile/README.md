# UnitySVC Labs

Service-provider catalog repos for the [UnitySVC](https://github.com/unitysvc) platform.

Each `unitysvc-services-*` repo holds the seller-side data (offerings, listings,
upstream access config, code examples, connectivity tests) for one provider.
Tracking issues for each provider live in
[`unitysvc-labs/unitysvc-labs/issues`](https://github.com/unitysvc-labs/unitysvc-labs/issues),
where status / type / reselling labels capture the operational state.

## Provider Catalog

The tables below auto-sync every six hours from the issue-tracker labels and
the per-repo CI runs.  See [`.github/workflows/sync-dashboard.yml`](https://github.com/unitysvc-labs/.github/blob/main/.github/workflows/sync-dashboard.yml).
One table per environment: **Production** is the canonical catalog (what end
users see); **Staging** previews changes before they ship.  Private
(in-development) providers are tracked but not listed here.

<!-- providers-start -->
| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟡 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 3 active | 3 published | 3 managed | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-aionlabs/pulls) |
| 🔴 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 8 rejected | 8 published | 8 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-anthropic/pulls) |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 4 active | 4 published | 4 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cerebras/pulls) |
| 🔴 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 16 active | 16 published | 16 byok | ❌ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | — | — | — | — | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-crofai/pulls) |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 1 active · 1 rejected | 2 published | 2 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | image_generation, llm | 8 active · 1 rejected | 9 published | 9 managed | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-fireworks/pulls) |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 7 active · 9 rejected | 16 published | 16 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | — | — | — | — | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 3 active | 3 published | 3 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-inception/pulls) |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 29 active · 30 rejected | 59 published | 59 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | — | — | — | — | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 managed | ✅ | — |
| 🔴 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | — | — | — | — | ❌ | [3](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🔴 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | embedding, llm | 51 active · 29 rejected | 80 published | 80 managed | ❌ | [2](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟡 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | content | 7 active · 1 rejected | 8 published | 3 byok · 5 managed | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-s3/pulls) |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 7 active · 2 rejected | 9 published | 9 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| 🟡 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | email | 3 active | 3 published | 2 byok · 1 managed | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-smtp/pulls) |
| — | **Total** (18 repos) | — | — | 140 active · 81 rejected | 221 published | 122 byok · 99 managed | — | 26 |
<!-- providers-end -->

_Last synced: 2026-05-25 01:57 UTC_

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
- **Listing type** — enrollment-mode counts: `managed` (seller provides
  upstream credentials), `byok` (customer supplies API key), `byoe`
  (customer supplies endpoint + key).
- **CI** — most recent CI run conclusion on `main`: ✅ success ·
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
