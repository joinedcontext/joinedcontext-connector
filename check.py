#!/usr/bin/env python3
"""Checks the joinedcontext open-data MCP connector against the Claude Connectors Directory rules.

Usage: python3 check.py [MCP_URL]   (default: the production connector)
Exit code 0 when every check passes. Standard library only.
"""
import json
import sys
import urllib.error
import urllib.request

MCP_URL = sys.argv[1] if len(sys.argv) > 1 else "https://api.smartcity.joinedcontext.com/api/mcp"
SITE = "https://opendata.smartcity.joinedcontext.com/en"
PAGES = ["connector", "privacy", "terms", "support"]  # docs, privacy policy, terms, support contact
HEADERS = {"content-type": "application/json", "accept": "application/json, text/event-stream"}

failures = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}{'  ' + detail if detail else ''}")
    if not ok:
        failures.append(name)


def rpc(method, params=None, rid=1):
    body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(MCP_URL, data=body, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode()
        if resp.headers.get_content_type() == "text/event-stream":
            raw = next(line[5:] for line in raw.splitlines() if line.startswith("data:"))
    msg = json.loads(raw)
    if "error" in msg:
        raise RuntimeError(f"{method}: {msg['error']}")
    return msg["result"]


def call(tool, arguments):
    result = rpc("tools/call", {"name": tool, "arguments": arguments}, rid=3)
    check(f"tools/call {tool}", not result.get("isError") and bool(result.get("content")))
    return result


def main():
    try:
        init = rpc("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "joinedcontext-claude-connector-check", "version": "1"},
        })
    except urllib.error.HTTPError as e:
        check("initialize without a token (no OAuth needed for open data)", False, f"HTTP {e.code}")
        return
    check("initialize without a token (no OAuth needed for open data)", "capabilities" in init,
          f"protocol {init.get('protocolVersion')}")

    tools = rpc("tools/list", rid=2)["tools"]
    check("tools/list returns tools", len(tools) > 0, f"{len(tools)} tools")
    for t in tools:
        ann = t.get("annotations", {})
        title = t.get("title") or ann.get("title")
        check(f"tool {t['name']}: title", bool(title), title or "missing")
        check(f"tool {t['name']}: readOnlyHint or destructiveHint",
              "readOnlyHint" in ann or "destructiveHint" in ann)
        check(f"tool {t['name']}: name at most 64 characters", len(t["name"]) <= 64)
    check("tool titles are unique",
          len({t.get("title") or t.get("annotations", {}).get("title") for t in tools}) == len(tools))

    # The example prompts in README.md, as the tool calls Claude makes for them.
    hits = call("search", {"query": "air quality", "limit": 3}).get("structuredContent", {}).get("hits", [])
    check("search finds air-quality datasets", len(hits) > 0, f"{len(hits)} hits")
    if hits:
        nxt = hits[0]["nextQuery"]
        call(nxt["tool"], nxt["arguments"])
    call("list_endpoints", {})
    call("search_documents", {"query": "doprava"})

    for page in PAGES:
        try:
            with urllib.request.urlopen(f"{SITE}/{page}", timeout=30) as resp:
                check(f"page /en/{page}", resp.status == 200)
        except urllib.error.URLError as e:
            check(f"page /en/{page}", False, str(e))


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, RuntimeError, KeyError, StopIteration, json.JSONDecodeError) as e:
        check("connector reachable and answering", False, repr(e))
    print(f"\n{len(failures)} failed" if failures else "\nall checks passed")
    sys.exit(1 if failures else 0)
