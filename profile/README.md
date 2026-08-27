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
### Production

| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟢 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 4 active | 4 published | 4 managed · 4 byok | ✅ | — |
| 🟢 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active | 10 published | 10 byok | ✅ | — |
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active | 37 published | 37 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-bedrock/pulls) |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active · 1 rejected | 3 published | 3 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cerebras/pulls) |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 16 active · 1 rejected · 1 rejected revision | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 18 active · 1 rejected · 1 rejected revision | 19 published | 19 managed · 19 byok | ✅ | — |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 2 active | 2 unlisted | 2 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🟢 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ✅ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 17 active · 1 rejected | 18 published | 18 managed · 18 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-fireworks/pulls) |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 5 active · 2 rejected | 7 published | 7 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 116 active · 23 rejected · 5 rejected revisions | 136 published · 3 unlisted | 139 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active · 1 draft revision | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 36 active · 4 rejected | 40 published | 40 byok | ✅ | — |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 25 active · 1 rejected · 2 rejected revisions | 26 published | 26 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 235 active | 235 published | 7 byok · 235 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🔴 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 12 draft | 12 published | 12 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-openai/pulls) |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 61 active · 5 rejected | 66 published | 66 managed · 66 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 4 active | 4 published | 4 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 828 active · 12 draft · 1 draft revision · 39 rejected · 9 rejected revisions | 854 published · 5 unlisted | 127 managed · 625 byok · 422 enrollable | — | 14 |

### Staging

| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟡 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 4 active · 2 draft revisions · 2 pending revisions | 4 published | 4 managed · 4 byok | ✅ | — |
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active · 10 pending revisions | 10 published | 10 byok | ✅ | — |
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active | 37 published | 37 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-bedrock/pulls) |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active · 1 draft · 1 draft revision · 1 pending revision | 3 published | 3 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cerebras/pulls) |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 2 draft revisions · 1 pending revision | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 19 active · 2 draft revisions · 11 pending revisions | 19 published | 19 managed · 19 byok | ✅ | — |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 2 active | 2 unlisted | 2 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🟢 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ✅ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 16 active · 1 review · 2 draft revisions · 1 pending · 6 pending revisions | 18 published | 18 managed · 18 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-fireworks/pulls) |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 5 active · 1 draft revision · 2 pending · 4 pending revisions | 7 published | 7 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 126 active · 1 review · 1 pending · 11 rejected · 6 rejected revisions · 1 review revision | 139 published | 139 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active · 1 pending revision | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 38 active · 2 draft revisions · 4 pending revisions · 2 rejected | 40 published | 40 byok | ✅ | — |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 25 active · 1 review · 1 pending revision · 25 review revisions | 26 published | 26 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 232 active · 3 review | 235 published | 7 byok · 235 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🟡 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 25 active · 1 pending · 25 pending revisions | 26 published | 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-openai/pulls) |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 66 active · 2 draft revisions · 4 pending revisions · 2 rejected revisions | 66 published | 66 managed · 66 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 4 active · 4 draft revisions | 4 published | 4 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 868 active · 1 draft · 6 review · 18 draft revisions · 5 pending · 70 pending revisions · 13 rejected · 8 rejected revisions · 26 review revisions | 871 published · 2 unlisted | 127 managed · 639 byok · 422 enrollable | — | 14 |
<!-- providers-end -->

_Last synced: 2026-08-27 05:11 UTC_

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
