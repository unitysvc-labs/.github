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
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active · 1 rejected revision | 37 published | 37 byok | ✅ | — |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active · 1 rejected | 3 published | 3 byok | ✅ | — |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 4 rejected revisions | 17 published | 17 byok | ✅ | — |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 19 active | 19 published | 19 managed · 19 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-crofai/pulls) |
| 🟢 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 3 active | 3 published | 3 byok | ✅ | — |
| 🟢 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ✅ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 17 active · 1 rejected | 18 published | 18 managed · 18 byok | ✅ | — |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 6 active · 6 rejected | 12 published | 12 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 127 active · 17 rejected · 5 rejected revisions | 144 published | 144 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟢 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 38 active | 38 published | 38 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 26 active | 26 published | 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 235 active | 235 published | 7 byok · 235 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🟢 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 12 active | 12 published | 12 byok | ✅ | — |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 73 active · 10 rejected | 83 published | 83 managed · 83 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟢 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 6 active | 6 published | 6 byok | ✅ | — |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 872 active · 35 rejected · 10 rejected revisions | 887 published | 144 managed · 653 byok · 422 enrollable | — | 8 |

### Staging

| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟢 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 4 active | 4 published | 4 managed · 4 byok | ✅ | — |
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active · 4 review revisions | 10 published | 10 byok | ✅ | — |
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active · 2 draft revisions · 1 rejected revision | 37 published | 37 byok | ✅ | — |
| 🟢 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active | 2 published | 2 byok | ✅ | — |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 1 draft revision · 3 rejected revisions | 17 published | 17 byok | ✅ | — |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 19 active · 2 review · 3 review revisions | 21 published | 21 managed · 21 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-crofai/pulls) |
| 🟢 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 3 active | 3 published | 3 byok | ✅ | — |
| 🟢 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ✅ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 17 active · 2 review · 1 rejected · 1 rejected revision · 1 review revision | 20 published | 20 managed · 20 byok | ✅ | — |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 8 active · 4 rejected | 12 published | 12 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 125 active · 2 review · 9 rejected · 2 rejected revisions · 27 review revisions | 136 published | 136 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active · 1 draft revision · 1 review revision | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 38 active · 2 rejected revisions · 3 review revisions | 38 published | 38 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 26 active · 2 review · 5 review revisions | 28 published | 28 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 235 active · 4 review · 3 rejected | 242 published | 10 byok · 242 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🟡 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 25 active · 1 rejected · 68 review revisions | 26 published | 26 byok | ✅ | — |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 75 active · 7 review · 7 rejected · 10 rejected revisions | 89 published | 89 managed · 89 byok | ✅ | [2](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 6 active · 1 rejected | 7 published | 7 byok | ✅ | — |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 887 active · 19 review · 4 draft revisions · 26 rejected · 19 rejected revisions · 112 review revisions | 912 published | 154 managed · 674 byok · 429 enrollable | — | 8 |
<!-- providers-end -->

_Last synced: 2026-08-30 20:09 UTC_

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
