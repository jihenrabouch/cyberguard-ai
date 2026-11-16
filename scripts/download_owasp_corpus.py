#!/usr/bin/env python3
"""Download the selected OWASP Cheat Sheet Series Markdown sources.

Run from the repository root:
    python scripts/download_owasp_corpus.py
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

BASE = "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/"

FILES = [
    "Authentication_Cheat_Sheet.md",
    "Authorization_Cheat_Sheet.md",
    "Cross_Site_Scripting_Prevention_Cheat_Sheet.md",
    "Cryptographic_Storage_Cheat_Sheet.md",
    "File_Upload_Cheat_Sheet.md",
    "HTTP_Headers_Cheat_Sheet.md",
    "Input_Validation_Cheat_Sheet.md",
    "Logging_Cheat_Sheet.md",
    "Multifactor_Authentication_Cheat_Sheet.md",
    "Password_Storage_Cheat_Sheet.md",
    "Query_Parameterization_Cheat_Sheet.md",
    "REST_Security_Cheat_Sheet.md",
    "SQL_Injection_Prevention_Cheat_Sheet.md",
    "Secrets_Management_Cheat_Sheet.md",
    "Server_Side_Request_Forgery_Prevention_Cheat_Sheet.md",
    "Session_Management_Cheat_Sheet.md",
    "Content_Security_Policy_Cheat_Sheet.md",
    "Threat_Modeling_Cheat_Sheet.md",
    "WebSocket_Security_Cheat_Sheet.md",
    "Vulnerable_Dependency_Management_Cheat_Sheet.md",
]

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw"
DEST.mkdir(parents=True, exist_ok=True)

def main():
    failures = []
    for filename in FILES:
        url = BASE + filename
        request = Request(url, headers={"User-Agent": "CyberGuide-educational-project/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                content = response.read()
                if response.status != 200 or not content.strip():
                    raise RuntimeError(f"HTTP {response.status} or empty file")
            (DEST / filename).write_bytes(content)
            print(f"[OK] {filename} ({len(content)} bytes)")
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            failures.append((filename, str(exc)))
            print(f"[ERROR] {filename}: {exc}")

    print(f"\nDownloaded: {len(FILES) - len(failures)}/{len(FILES)}")
    if failures:
        print("Some files could not be downloaded. Check the official repository and retry.")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
