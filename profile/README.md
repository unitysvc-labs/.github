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
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active | 10 published | 10 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-anthropic/pulls) |
| 🟢 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active | 37 published | 37 byok | ✅ | — |
| 🟢 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active | 2 published | 2 byok | ✅ | — |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 1 rejected revision | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🔴 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | — | — | — | — | ❌ | — |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 1 active | 1 published | 1 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🔴 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ❌ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 28 active · 6 rejected · 1 rejected revision | 16 published | 34 managed · 16 byok | ✅ | — |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 7 active · 4 rejected | 11 published | 11 byok | ✅ | — |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 2 active | 1 published | 1 managed · 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 133 active · 4 rejected · 3 rejected revisions | 137 published | 137 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟢 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active | 1 published | 1 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 30 active | 30 published | 30 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 17 active | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 189 active | 150 published | 23 managed · 166 byok · 125 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 239 active · 3 rejected | 242 published | 9 byok · 242 enrollable | ✅ | — |
| 🟢 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 26 active | 26 published | 26 byok | ✅ | — |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 85 active · 1 rejected | 86 published | 86 managed · 86 byok | ✅ | — |
| 🟢 | [Replace per-repo LLM service templates with a platform-hosted system template](https://github.com/unitysvc-labs/unitysvc-labs/issues/75) | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | mcp | 16 active | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🔴 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ❌ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 6 active · 1 rejected | 7 published | 7 byok | ✅ | — |
| 🟡 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 6 active · 1 rejected revision | 5 published | 2 managed · 4 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 885 active · 19 rejected · 6 rejected revisions | 825 published | 170 managed · 601 byok · 380 enrollable | — | 6 |

### Staging

| Status | Provider | Repo | Type | Lifecycle | Visibility | Listing type | CI | Open PRs |
|---|---|---|---|---|---|---|---|---|
| 🟢 | [Aion Labs](https://github.com/unitysvc-labs/unitysvc-labs/issues/9) | [`unitysvc-services-aionlabs`](https://github.com/unitysvc-labs/unitysvc-services-aionlabs) | llm | 4 active | 4 published | 4 managed · 4 byok | ✅ | — |
| 🟡 | [Anthropic](https://github.com/unitysvc-labs/unitysvc-labs/issues/21) | [`unitysvc-services-anthropic`](https://github.com/unitysvc-labs/unitysvc-services-anthropic) | llm | 10 active | 10 published | 10 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-anthropic/pulls) |
| 🟢 | bedrock | [`unitysvc-services-bedrock`](https://github.com/unitysvc-labs/unitysvc-services-bedrock) | llm | 37 active | 37 published | 37 byok | ✅ | — |
| 🟢 | [Cerebras](https://github.com/unitysvc-labs/unitysvc-labs/issues/22) | [`unitysvc-services-cerebras`](https://github.com/unitysvc-labs/unitysvc-services-cerebras) | llm | 2 active | 2 published | 2 byok | ✅ | — |
| 🟡 | [Cohere](https://github.com/unitysvc-labs/unitysvc-labs/issues/24) | [`unitysvc-services-cohere`](https://github.com/unitysvc-labs/unitysvc-services-cohere) | embedding, llm | 17 active · 1 rejected revision | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-cohere/pulls) |
| 🔴 | [Crof AI](https://github.com/unitysvc-labs/unitysvc-labs/issues/11) | [`unitysvc-services-crofai`](https://github.com/unitysvc-labs/unitysvc-services-crofai) | llm | 21 active · 21 rejected revisions | — | 21 managed | ❌ | — |
| 🟡 | [DeepSeek](https://github.com/unitysvc-labs/unitysvc-labs/issues/25) | [`unitysvc-services-deepseek`](https://github.com/unitysvc-labs/unitysvc-services-deepseek) | llm | 1 active | 1 published | 1 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-deepseek/pulls) |
| 🔴 | demo | [`unitysvc-services-demo`](https://github.com/unitysvc-labs/unitysvc-services-demo) | content, email, llm, notification, proxy | 20 active | — | 9 managed · 6 byok · 6 enrollable | ❌ | — |
| 🟡 | [Fireworks](https://github.com/unitysvc-labs/unitysvc-labs/issues/10) | [`unitysvc-services-fireworks`](https://github.com/unitysvc-labs/unitysvc-services-fireworks) | embedding, llm | 28 active · 6 rejected · 1 rejected revision | 16 published | 34 managed · 16 byok | ✅ | — |
| 🟡 | [Groq](https://github.com/unitysvc-labs/unitysvc-labs/issues/7) | [`unitysvc-services-groq`](https://github.com/unitysvc-labs/unitysvc-services-groq) | llm | 7 active · 4 rejected | 11 published | 11 byok | ✅ | — |
| 🟢 | [HTTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/27) | [`unitysvc-services-http`](https://github.com/unitysvc-labs/unitysvc-services-http) | proxy | 2 active | 1 published | 1 managed · 1 byok · 1 enrollable | ✅ | — |
| 🟡 | [Hugging Face](https://github.com/unitysvc-labs/unitysvc-labs/issues/28) | [`unitysvc-services-huggingface`](https://github.com/unitysvc-labs/unitysvc-services-huggingface) | llm | 140 active · 2 rejected · 4 rejected revisions | 142 published | 142 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-huggingface/pulls) |
| 🟢 | [Inception](https://github.com/unitysvc-labs/unitysvc-labs/issues/29) | [`unitysvc-services-inception`](https://github.com/unitysvc-labs/unitysvc-services-inception) | llm | 1 active | 1 published | 1 byok | ✅ | — |
| 🟡 | [Mistral](https://github.com/unitysvc-labs/unitysvc-labs/issues/30) | [`unitysvc-services-mistral`](https://github.com/unitysvc-labs/unitysvc-services-mistral) | embedding, llm | 30 active · 12 rejected revisions | 30 published | 30 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-mistral/pulls) |
| 🟡 | [Nebius Cloud](https://github.com/unitysvc-labs/unitysvc-labs/issues/20) | [`unitysvc-services-nebius`](https://github.com/unitysvc-labs/unitysvc-services-nebius) | embedding, llm | 17 active | 17 published | 17 byok | ✅ | [1](https://github.com/unitysvc-labs/unitysvc-services-nebius/pulls) |
| 🟢 | [Notify](https://github.com/unitysvc-labs/unitysvc-labs/issues/31) | [`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify) | notification | 189 active | 150 published | 23 managed · 166 byok · 125 enrollable | ✅ | — |
| 🟢 | [ntfy](https://github.com/unitysvc-labs/unitysvc-labs/issues/32) | [`unitysvc-services-ntfy`](https://github.com/unitysvc-labs/unitysvc-services-ntfy) | notification | 1 active | 1 published | 1 enrollable | ✅ | — |
| 🟡 | [Ollama](https://github.com/unitysvc-labs/unitysvc-labs/issues/33) | [`unitysvc-services-ollama`](https://github.com/unitysvc-labs/unitysvc-services-ollama) | embedding, llm | 239 active · 3 rejected · 2 rejected revisions | 235 published · 7 unlisted | 9 byok · 242 enrollable | ✅ | — |
| 🟢 | openai | [`unitysvc-services-openai`](https://github.com/unitysvc-labs/unitysvc-services-openai) | llm | 26 active | 26 published | 26 byok | ✅ | — |
| 🟡 | [Parasail](https://github.com/unitysvc-labs/unitysvc-labs/issues/34) | [`unitysvc-services-parasail`](https://github.com/unitysvc-labs/unitysvc-services-parasail) | llm | 87 active · 1 rejected | 88 published | 88 managed · 88 byok | ✅ | — |
| 🟡 | [Replace per-repo LLM service templates with a platform-hosted system template](https://github.com/unitysvc-labs/unitysvc-labs/issues/75) | [`unitysvc-services-mcp`](https://github.com/unitysvc-labs/unitysvc-services-mcp) | mcp, proxy | 16 active · 1 rejected revision | 16 published | 5 managed · 11 byok | ✅ | — |
| 🟢 | resp | [`unitysvc-services-resp`](https://github.com/unitysvc-labs/unitysvc-services-resp) | proxy | 6 active | 6 published | 6 managed | ✅ | — |
| 🔴 | [S3](https://github.com/unitysvc-labs/unitysvc-labs/issues/36) | [`unitysvc-services-s3`](https://github.com/unitysvc-labs/unitysvc-services-s3) | proxy | 2 active | 2 published | 2 byok · 2 enrollable | ❌ | — |
| 🟡 | [SambaNova](https://github.com/unitysvc-labs/unitysvc-labs/issues/37) | [`unitysvc-services-sambanova`](https://github.com/unitysvc-labs/unitysvc-services-sambanova) | llm | 6 active · 1 rejected | 7 published | 7 byok | ✅ | — |
| 🟡 | [SMTP](https://github.com/unitysvc-labs/unitysvc-labs/issues/38) | [`unitysvc-services-smtp`](https://github.com/unitysvc-labs/unitysvc-services-smtp) | notification, proxy | 6 active · 1 rejected revision | 5 published | 2 managed · 4 byok · 3 enrollable | ✅ | — |
| — | **Total** (25 repos) | — | — | 915 active · 17 rejected · 43 rejected revisions | 825 published · 7 unlisted | 193 managed · 608 byok · 380 enrollable | — | 6 |
<!-- providers-end -->

_Last synced: 2026-09-18 10:07 UTC_

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
