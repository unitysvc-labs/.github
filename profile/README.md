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
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active · 10 rejected revisions | 10 published | 10 byok | ✅ | — |
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 36 active · 1 rejected · 36 rejected revisions | 37 published | 37 byok | ✅ | — |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active · 1 rejected · 2 rejected revisions | 3 published | 3 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cerebras/pulls) |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 16 active · 1 rejected · 11 rejected revisions | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 17 active · 9 rejected · 17 rejected revisions | 26 published | 26 managed · 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-crofai/pulls) |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 2 active · 2 rejected revisions | 2 published | 2 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🟡 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-demo/pulls) |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 16 active · 2 rejected · 15 rejected revisions | 18 published | 18 managed · 18 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-fireworks/pulls) |
| 🔴 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 5 active · 2 rejected · 5 rejected revisions | 7 unlisted | 7 byok | ❌ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 87 active · 49 rejected | 136 unlisted | 136 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active · 1 rejected revision | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 33 active · 7 rejected · 29 rejected revisions | 40 unlisted | 40 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 21 active · 5 rejected · 20 rejected revisions | 26 published | 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| ⚪ | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | 🟡 | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 232 active · 3 rejected · 13 rejected revisions | 235 published | 10 byok · 235 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 34 active · 34 rejected · 2 rejected revisions | 68 published | 68 managed · 68 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 3 active · 1 rejected · 3 rejected revisions | 4 published | 4 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (24 repos) | — | — | 758 active · 115 rejected · 166 rejected revisions | 670 published · 183 unlisted | 136 managed · 622 byok · 422 enrollable | — | 13 |

### Staging

| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟡 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 4 active · 4 review revisions | 4 published | 4 managed · 4 byok | ✅ | — |
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active · 10 review revisions | 10 published | 10 byok | ✅ | — |
| 🟡 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active · 37 review revisions | 37 published | 37 byok | ✅ | — |
| 🟡 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active · 1 rejected · 2 review revisions | 3 published | 3 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cerebras/pulls) |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 5 draft revisions · 6 rejected revisions · 26 review revisions | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🟡 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 17 active · 9 rejected · 17 review revisions | 26 published | 26 managed · 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-crofai/pulls) |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 2 active | 2 published | 2 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🟡 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active · 3 draft revisions · 3 review revisions | — | 9 managed · 6 byok · 6 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-demo/pulls) |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 16 active · 1 draft revision · 2 rejected · 16 review revisions | 18 published | 18 managed · 18 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-fireworks/pulls) |
| 🔴 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 4 active · 3 rejected · 4 review revisions | 7 published | 7 byok | ❌ | [1](https://github.com/unitysvc-labs/unitysvc-services-groq/pulls) |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 1 active | 1 published | 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 102 active · 34 rejected · 16 rejected revisions · 86 review revisions | 136 published | 136 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟡 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active · 1 review revision | 1 published | 1 byok | ✅ | — |
| 🟢 | mcp | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | proxy | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 36 active · 4 draft revisions · 4 rejected · 7 rejected revisions · 29 review revisions | 40 published | 40 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 25 active · 1 draft revision · 1 rejected · 2 rejected revisions · 23 review revisions | 26 published | 26 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| ⚪ | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 188 active | 188 published | 188 byok · 174 enrollable | 🟡 | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 232 active · 196 draft revisions · 3 rejected · 12 rejected revisions · 224 review revisions | 235 published | 10 byok · 235 enrollable | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-ollama/pulls) |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 36 active · 32 rejected · 8 rejected revisions · 28 review revisions | 68 published | 68 managed · 68 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-parasail/pulls) |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🟢 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ✅ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 4 active · 4 review revisions | 4 published | 4 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-sambanova/pulls) |
| 🟢 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 5 active | 5 published | 5 byok · 3 enrollable | ✅ | — |
| — | **Total** (24 repos) | — | — | 784 active · 210 draft revisions · 89 rejected · 51 rejected revisions · 514 review revisions | 853 published | 136 managed · 622 byok · 422 enrollable | — | 13 |
<!-- providers-end -->

_Last synced: 2026-08-25 12:20 UTC_

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
