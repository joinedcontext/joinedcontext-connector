# Directory submission sheet

Paste these answers into <https://claude.ai/directory/manage> → **Submit new** → **MCP connector**. You need any paid Claude plan. Run `python3 check.py` first; submit only when it prints `all checks passed`.

## Connection

- URL: `https://api.smartcity.joinedcontext.com/api/mcp`
- Users connect to different URLs: no

## Tools

The portal syncs the 18 tools from the server. All 18 are read-only. If any tool shows a missing title, wait for T-4732 to reach prod and click **Sync** again.

## Listing

- Server name: `Joinedcontext Open Data`
- One-liner (200 characters max): `Search and read open data from European cities and regions: air quality, transport, schools, places, sensor history and the publishers' own pages.`
- Description (2,000 characters max):

  > Joinedcontext Open Data connects Claude to the open data that cities and regions publish on the joinedcontext platform, starting with Banská Bystrica, the Banská Bystrica Self-Governing Region, Žilina, Prague and Helsinki.
  >
  > Ask in English or Slovak. Claude finds the right dataset, reads the current values or their history, and cites the publisher. It can search air quality, public transport stops and timetables, schools, points of interest, bridges, indicators and sensor history, filter by place and time, and search the publishers' own announcements and pages.
  >
  > Every tool is read-only and returns only what a publisher released as open data. The connector needs no account and no login.
- Categories: Data & Analytics; Government; Research
- Documentation URL: `https://opendata.smartcity.joinedcontext.com/en/connector`
- Privacy policy URL: `https://opendata.smartcity.joinedcontext.com/en/privacy`
- Support contact: `hello@joinedcontext.com`
- Icon: the joinedcontext logo in the `assets` folder (512 × 512 PNG)
- URL slug (permanent): `joinedcontext-open-data`

## Use cases

- Primary use cases: Citizens, journalists and city staff ask questions about their city's open data, such as "how is the air in Banská Bystrica today" or "which schools are near this address", and get answers that cite the dataset and publisher. Developers find the right dataset and its API call for their own app.
- What users need before connecting: nothing; no account, plan or setup.
- Reads or writes: reads only.

## Company

- Company: joinedcontext
- Website: `https://joinedcontext.com`
- Primary contact: Marek Mraz, `hello@joinedcontext.com`

## Authentication

- No authentication. The server serves public open data and answers every tool call without a token.

## Data handling

- Underlying API: our own (the joinedcontext platform), serving data its publishers released as open data.
- Personal health data: no.
- Sponsored content: no.

## Test & launch

- Test account: none needed. Reviewers add the URL as a custom connector (Settings → Connectors → Add custom connector) and can call every tool with no credentials.
- Steps for reviewers: add the connector, then try the five example prompts in README.md. Each one calls a different tool.
- Confirm: every tool has been run, through `check.py` and as a custom connector in Claude.

## Compliance

Read and accept the seven acknowledgments. The connector makes no financial transactions, generates no AI media, collects no conversation data, and its documentation is public.
