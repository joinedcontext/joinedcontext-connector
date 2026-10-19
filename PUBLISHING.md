# Publishing manual

One repository holds everything for both stores:

| File | Claude | ChatGPT / Codex |
|---|---|---|
| `.mcp.json` | the MCP server, used by the plugin | the MCP server, used by the plugin |
| `.claude-plugin/plugin.json` | plugin manifest | |
| `.claude-plugin/marketplace.json` | makes this repo a plugin marketplace | |
| `.codex-plugin/plugin.json` | | plugin manifest with the store listing (`interface`) |
| `skills/open-data/SKILL.md` | how to use the tools well | the same skill |
| `assets/icon.png` | directory icon | logo and composer icon |
| `SUBMISSION.md` | answers for the Claude directory portal | |
| `openai-test-cases.json` | | the 5 positive and 3 negative review cases |
| `check.py` | the directory rules, tested against the live server | the same |

## 0. Before any submission

1. T-4732 is on prod: every tool has a title and all three hints.
2. `python3 check.py` prints `all checks passed`.
3. `claude plugin validate .` prints `Validation passed`.

## 1. GitHub

The repository is public at `github.com/marek-mraz/joinedcontext-connector`. The `check` workflow runs `check.py` on every push and once a day, so a broken server shows as a red badge before a reviewer finds it.

## 2. Claude

### 2.1 Everyone in our organization, today

**Admin settings → Connectors → Add custom connector**: name `joinedcontext open data`, URL `https://api.smartcity.joinedcontext.com/api/mcp`. Members turn it on under **Settings → Connectors**. Nobody logs in.

### 2.2 Claude Code users, today

```bash
/plugin marketplace add marek-mraz/joinedcontext-connector
/plugin install joinedcontext-open-data@joinedcontext
```

The plugin brings the MCP server and the `open-data` skill. To make it the default for a repository, commit this to that repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "joinedcontext": { "source": { "source": "github", "repo": "marek-mraz/joinedcontext-connector" } }
  },
  "enabledPlugins": { "joinedcontext-open-data@joinedcontext": true }
}
```

### 2.3 The public Connectors Directory

1. Open <https://claude.ai/directory/manage>, then **Submit new → MCP connector**. Any paid plan can submit.
2. Paste the answers from `SUBMISSION.md` step by step and upload `assets/icon.png`.
3. Submit. Anthropic scans the server and lists it as a Community connector. Status and reviewer feedback appear in the same portal; escalations go to <mcp-review@anthropic.com>.

### 2.4 The plugin directory (optional)

In the same portal choose **Submit new → Plugin** and give this repository. The connector listing (2.3) and the plugin can be paired there.

## 3. ChatGPT and Codex

OpenAI's Plugins Directory serves ChatGPT and Codex from one submission.

### 3.1 Account

1. In <https://platform.openai.com/settings/organization/general>, finish **business verification** for joinedcontext. Submission is blocked without it.
2. Only an organization Owner, or a member with **Apps Management Write**, can submit.

### 3.2 Domain verification

1. In <https://platform.openai.com/plugins>, open the draft and its **MCPs** tab. **Connect** shows a challenge token.
2. Give the token to the supervisor (it is public, not a secret). The deployer serves it as plain text at `https://api.smartcity.joinedcontext.com/.well-known/openai-apps-challenge`, with only the token in the body.
3. Check: `curl -s https://api.smartcity.joinedcontext.com/.well-known/openai-apps-challenge` prints exactly the token.

### 3.3 Package

```bash
git archive --format=zip -o joinedcontext-open-data-1.0.0.zip HEAD
```

`.gitattributes` leaves the CI, the check and the submission notes out of the ZIP. Raise `version` in both `plugin.json` files before each new upload.

### 3.4 Submit

1. <https://platform.openai.com/plugins> → **Upload new or existing plugin**, choose the **developer identity** `joinedcontext`, upload the ZIP.
2. **Metadata & Skills**: fix any issue it lists, upload again.
3. **MCPs** → **Connect**: URL `https://api.smartcity.joinedcontext.com/api/mcp`, authentication **none**, complete the domain check, wait for the tool scan.
4. **Review information → Review details**: paste the cases from `openai-test-cases.json`. Reviewer credentials: none needed. Add the demo video URL (a 1–2 minute screen recording of the three `defaultPrompt` questions in ChatGPT with the app on, link readable by anyone).
5. **Submit for review** and accept the attestations. Feedback arrives by email.
6. After approval: open the approved version and **Publish plugin**.

### 3.5 Before the listing, for our own workspace

A ChatGPT Business or Enterprise admin can add the server as a custom app (MCP URL above, no authentication) in the workspace settings, and members turn it on. On a personal plan, developer mode allows the same for one account.

## 4. After publishing

- Change a tool: run `check.py` against dev, then prod, then use **Rescan** in OpenAI's portal and **Sync** in Claude's.
- Change the listing text: edit `SUBMISSION.md` or `.codex-plugin/plugin.json`, raise the version, and resubmit.
