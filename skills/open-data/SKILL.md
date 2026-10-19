---
name: open-data
description: Answer questions about city and regional open data (air quality, transport, schools, places, sensors, history, publishers' announcements) for Banská Bystrica, the Banská Bystrica region, Žilina, Prague and Helsinki with the joinedcontext MCP tools. Use when the user asks about such data or wants a script that downloads it.
---

# Joinedcontext Open Data

1. Start with the `search` tool: put the question in `query` (Slovak or English), narrow with `place`, `domain` or `type`.
2. Each hit names its Endpoint and a `nextQuery`: call that tool with those arguments to read the values.
3. History: `query_temporal` on the same Endpoint, with a time range.
4. Announcements and web pages of a publisher: `search_documents`.
5. Cite the dataset title and publisher in the answer. Never guess a value the tools did not return.

For a script, read the Endpoint's URLs with `get_endpoint` and write code that calls those public URLs.
