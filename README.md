# Joinedcontext Open Data connector

A remote MCP connector and plugin that lets Claude, ChatGPT and Codex search and read the open data that Slovak and other European cities and regions publish on the joinedcontext platform: air quality, transport, schools, points of interest, sensor history, and the publishers' own web pages.

| | |
|---|---|
| Server URL | `https://api.smartcity.joinedcontext.com/api/mcp` |
| Transport | Streamable HTTP |
| Authentication | none: the connector serves open data only |
| Tools | 18, all read-only |
| Documentation | <https://opendata.smartcity.joinedcontext.com/en/connector> |
| Privacy policy | <https://opendata.smartcity.joinedcontext.com/en/privacy> |
| Terms of use | <https://opendata.smartcity.joinedcontext.com/en/terms> |
| Support | <https://opendata.smartcity.joinedcontext.com/en/support>, <hello@joinedcontext.com> |

## Add it to Claude

**For the whole organization (Team or Enterprise):** an Owner opens **Admin settings → Connectors → Add custom connector**, names it `Joinedcontext Open Data` and pastes the server URL. Every member then finds it under **Settings → Connectors** and turns it on. Nobody logs in.

**For yourself (Pro or Max):** **Settings → Connectors → Add custom connector**, the same name and URL.

**Claude Code, as a plugin (MCP server plus a usage skill):**

```bash
/plugin install joinedcontext-open-data --marketplace marek-mraz-jc/joinedcontext-connector
```

**Claude Code, the server only:**

```bash
claude mcp add --transport http joinedcontext https://api.smartcity.joinedcontext.com/api/mcp
```

Once the directory lists it, everyone can add it from **Settings → Connectors → Browse connectors** instead.

## Example prompts

Each one exercises a different tool.

1. "Which air-quality datasets do you have for Banská Bystrica? Show me the latest readings." (`search`, then `query_entities`)
2. "List the data endpoints you can read and what types each one holds." (`list_endpoints`, `get_endpoint`)
3. "What did the region announce about road closures and traffic? Quote the source page." (`search_documents`)
4. "How did PM10 in Banská Bystrica change over the last week?" (`query_temporal`)
5. "Which bus stops are within 500 m of the Žilina town centre?" (`query_entities` with a geo filter)

## Tools

All tools are read-only (`readOnlyHint: true`, `destructiveHint: false`) and return only data its publishers released as open data.

| Tool | What it does |
|---|---|
| `search` | Ranks datasets for a question by title, description (sk, en), type, domain, place and publisher |
| `list_endpoints`, `get_endpoint` | The readable data endpoints, and one endpoint whole |
| `search_documents` | Searches the publishers' own web pages |
| `query_entities`, `get_entity` | Reads current values, with type, attribute, text and geo filters |
| `query_temporal`, `retrieve_temporal` | Reads history |
| `list_types`, `get_type`, `list_type_details`, `list_attributes`, `get_attribute`, `list_attribute_details`, `get_attribute_value` | Describe the data model |
| `summarize`, `describe_access`, `describe_schema` | Summaries, access rules and schemas of an endpoint |

## Check

`check.py` runs the directory's requirements against the live server: no-token `initialize`, a title and a read-only or destructive hint on every tool, tool names of 64 characters or fewer, the example prompts' tool calls, and the documentation, privacy, terms and support pages. It uses the Python standard library only.

```bash
python3 check.py                                            # production
python3 check.py https://api.dev.joinedcontext.com/api/mcp  # dev
```

The GitHub workflow runs it on every push and once a day.

## Submit

[PUBLISHING.md](PUBLISHING.md) is the step-by-step manual for Claude and ChatGPT. [SUBMISSION.md](SUBMISSION.md) holds every answer the developer portal at <https://claude.ai/directory/manage> asks for, and [assets/icon.png](assets/icon.png) the icon.

## Privacy

The connector needs no account and sets no cookie. It receives each tool call's arguments and the caller's IP address. The edge counts calls per IP address in memory to limit their rate; the services write requests to container logs, which the server rotates and nobody archives or sends to analytics. What a person types stays with their assistant. Full policy: <https://opendata.smartcity.joinedcontext.com/en/privacy>. Contact: <hello@joinedcontext.com>.
