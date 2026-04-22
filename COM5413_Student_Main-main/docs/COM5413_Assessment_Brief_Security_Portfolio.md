# The Benji Protocol
## COM5413 — Programming for Cyber Security
### Assessment Brief: The Security Portfolio

| Field | Detail |
|-------|--------|
| **Module Code** | COM5413 |
| **Level** | HE5 (Second Year Undergraduate) |
| **Weighting** | 100% — Single Portfolio Submission |
| **Assessment Title** | The Benji Protocol: Security Automation Portfolio |
| **Assessment Type** | Practical Portfolio and Controlled Capstone |
| **Submission** | GitHub Classroom repository URL — submitted via Moodle |

---

> **You are Benji Dunn. Technical Intelligence Operative.**
>
> Over the next five weeks you will build a field toolkit from scratch — four Python tools — then deploy only that toolkit on a live target in a controlled, timed operation.
>
> **The code you write in Weeks 1–4 is the code you will use in Week 5. There is no practice mode.**

---

## 1. Assessment Overview

This module is assessed through a single portfolio submission. The portfolio has two parts that are directly connected — Part 1 builds the instruments; Part 2 deploys them.

| Week | Name | In One Line |
|------|------|-------------|
| W1 — The Scene | The Evidence Collector | Pull the logs. Find what happened. |
| W2 — The Map | The Network Cartographer | Scan the target. Identify every open door. |
| W3 — The Key | The Access Validator | Test credentials. Find the way in. |
| W4 — The Surface | The Web Enumerator | Read what the web layer is saying. |
| W5 — The Mission | The Vulnerability Hunt | 4 hours. One target. Unseen scenario. |

| Part | Description |
|------|-------------|
| **Part 1 — The Toolkit (Weeks 1–4)** | Four Python tools built week by week and tested against IMF Field Tests (auto-graded unit tests). Marks are earned through passing test results committed progressively to your repository. |
| **Part 2 — The Mission (Week 5)** | A four-hour in-class controlled assessment. You receive an unseen scenario. You use only your toolkit to diagnose a live target, write an exploit, retrieve the Flag, and remediate the vulnerability. Nothing is installed on the day — you bring your tools. |

---

## 2. Part 1 — The Toolkit (Weeks 1–4)

Each tool must be command-line executable, accept arguments using `argparse`, and handle errors without crashing. The technical specification in Appendix A is your contract with the auto-grader.

> **IMF Field Tests:** Each week a test suite (`field_tests/test_taskN.py`) is released at the start of Session A. Run these locally with `pytest`. The same tests run at marking. Your test results — committed progressively — are the primary evidence of Part 1 quality.

---

### Week 1 — The Scene: The Evidence Collector (`log_parser.py`)

**Objective:** Parse a Linux `auth.log` file to identify Indicators of Compromise. Extract failed authentication attempts and produce a structured CSV evidence report.

**Operational value:** Used in the Mission to verify your own attack footprint and analyse the target's logs after exploitation.

Requirements:
- Accept a log file path via `argparse`. Never use `input()`.
- Use `re` to identify lines containing `"Failed password"` or `"Invalid user"`.
- Extract: timestamp, IP address, and user account from each match.
- Output CSV to `suspects.csv` (or `--output` path). Headers must be exactly: `Timestamp, IP_Address, User_Account`
- De-duplicate entries. Two records are duplicates if they share the same Timestamp, IP_Address, and User_Account. Handle missing files and empty results without crashing.

---

### Week 2 — The Map: The Network Cartographer (`scan.py`)

**Objective:** Build a threaded TCP port scanner that identifies open services and grabs service banners.

**Operational value:** The first step of every Mission scenario. The banner tells you the version; the version points to the CVE.

Requirements:
- Accept a target IP and port range or list (e.g. `1-1024` or `21,22,80`).
- Use Python's `socket` library only — do not wrap Nmap or any external scanner.
- Implement connection timeout (default 0.5 seconds).
- Attempt to receive the service banner on each open port.
- Use `ThreadPoolExecutor` for concurrent scanning.
- Output JSON saved to `recon_results.json` and printed to stdout.

---

### Week 3 — The Key: The Access Validator (`brute.py`)

**Objective:** Build a targeted credential testing tool for SSH and FTP services.

**Operational value:** Confirms whether default or weak credentials are in use — one of the most common real-world findings.

Requirements:
- Accept: target IP, `--service` (ssh|ftp), `--user`, `--wordlist` (path to file).
- SSH: use `paramiko`. FTP: use `ftplib`. No other libraries for authentication logic.
- Include `time.sleep(0.1)` between **every** attempt. The field test checks for this in source. It prevents denial-of-service behaviour.
- Handle empty lines, whitespace, and non-ASCII in the wordlist without crashing.
- Print on success: `[+] SUCCESS: Password found: <password>`
- Log every attempt to a file — this is your evidence trail.

---

### Week 4 — The Surface: The Web Enumerator (`web_enum.py`)

**Objective:** Automate HTTP reconnaissance. Read what the server is already broadcasting.

**Operational value:** Identifies web technology versions and exposes developer notes left in source — both are common exploitation starting points.

Requirements:
- Accept a target URL via `argparse`.
- Use `requests` for the HTTP GET and header analysis. Extract `Server` and `X-Powered-By`.
- Use `BeautifulSoup` (`bs4`) to extract all HTML comments (`<!-- -->`).
- Probe sensitive paths (`/robots.txt`, `/admin`, `/phpmyadmin`, `/.git`) and report HTTP status codes.
- Set a request timeout — never allow the script to hang.

---

## 3. Part 2 — The Mission (Week 5)

> *"The kit is packed. The mission is live. Ethan is on the roof. Benji has one job: make sure everything works first time."*

The Mission is a four-hour in-class controlled assessment. You arrive with your toolkit. You receive an unseen scenario. You have four hours.

### The Four Phases

1. **Diagnose** — Run your toolkit against the target. Identify the vulnerable service and its version.
2. **Exploit** — Write a Python script that triggers the vulnerability and retrieves the Flag. No Metasploit. No automated exploit frameworks. You write the logic.
3. **Remediate** — Write a defensive script or configuration patch that closes the vulnerability while keeping the service running.
4. **Submit** — Push your code and a completed `REPORT.md` to GitHub before the timer ends. Tag: `hunt-final`.

### What You Will Submit

- `exploit.py` — working Python script that retrieves the Flag without manual steps.
- `fix.py` — remediation script or clearly commented configuration patch.
- `REPORT.md` — reconnaissance findings, the Flag, exploit approach, and remediation rationale.
- `AI_LOG.md` — updated before the session ends.
- `requirements.txt` — current as of submission.

### Non-Negotiable Constraints

- No Metasploit. No automated exploit frameworks. No tooling that generates the exploit logic.
- You must write the Python connection and trigger logic yourself. Code you cannot explain will be referred for academic integrity review.
- If you retrieve the Flag manually but your script does not automate it, your Part 2 mark is capped at Pass level.
- No commits after the session closes. The GitHub Classroom timestamp is definitive. Commits after the stated cutoff render those changes void.

---

## 4. Submission & Repository Requirements

### Repository Structure

| Path | Contents |
|------|----------|
| `toolkit/task1_evidence_collector/` | `log_parser.py` and `suspects.csv` |
| `toolkit/task2_network_cartographer/` | `scan.py` and `recon_results.json` |
| `toolkit/task3_access_validator/` | `brute.py` |
| `toolkit/task4_web_enumerator/` | `web_enum.py` |
| `field_tests/` | IMF Field Test suites — released weekly. Do not modify. |
| `vulnerability_hunt/` | `exploit.py`, `fix.py`, `REPORT.md` |
| `docs/build.md` | Running build log — updated every session |
| `AI_LOG.md` | Mandatory AI usage audit |
| `requirements.txt` | Current pip dependencies |
| `README.md` | Repository overview |

### Git History Requirement

Your commit history is part of your submission.

- A repository showing progressive development — commits at each build stage, weekly tags, meaningful messages — evidences professional practice.
- A repository where four tools appear in a single commit shortly before the deadline evidences the opposite. This is reflected in the Professional Practice component of your mark.
- Required tags: `w1`, `w2`, `w3`, `w4`, `hunt-final`.

### The Build Log — `docs/build.md`

A running technical journal updated every session. Not an essay. Cover: what you built, what broke, how you fixed it, what your tool output on the target. During the Mission, update it in real time.

### The AI Transparency Rule

You may use GenAI tools to debug, explain, or refactor code. Document every substantive use in `AI_LOG.md`:

| Field | Example |
|-------|---------|
| **Prompt Used** | "Write a regex to extract IP addresses from auth.log." |
| **AI Output** | Provided pattern `\b(?:\d{1,3}\.){3}\d{1,3}\b` with explanation. |
| **My Verification** | Tested against fixture — pattern missed IPs mid-line. Adjusted and re-tested. |

> **Prohibited:** Pasting the Mission scenario and asking for the solution. Code you cannot explain that is not in AI_LOG.md will be referred for academic integrity review.

---

## 5. Grading Rubric

| Grade Band | Part 1: The Toolkit | Part 2: The Mission | Professional Practice |
|---|---|---|---|
| **80%+ Exceptional** | Tools are classes/modules. Importable. Highly robust error handling. | Single-command exploit. Fully automated remediation: patches and verifies. | DevSecOps hygiene. Feature branches. Deep AI critique documented. PEP8 throughout. |
| **70–79% Distinction** | Robust scripts. Good input validation. Pass all field tests efficiently. | Reliable flag retrieval via script. Remediation is valid config or detailed script logic. | Clear commit messages. AI_LOG shows verification of security implications. |
| **60–69% Merit** | Functional tools. Passes field tests. Some hardcoding removed. | Flag retrieved. Script needed manual tweaking during the Hunt. Remediation is descriptive. | Regular commits throughout. AI usage documented with context. |
| **50–59% Pass** | Basic scripts. Passes more than half of field tests. | Vulnerability found. Manual tooling used to retrieve flag; script attempted the logic. | Code on GitHub. AI_LOG minimal. Commit messages generic. |
| **Below 40% Fail** | Tools fail tests or won't execute. | Flag not retrieved. No remediation attempt. | No meaningful Git history. AI_LOG absent. |

> **On the rubric bands:** The distinction between Merit and Distinction in Part 2 is not whether the Flag was retrieved — at Merit level it has been. It is the degree of automation and the quality of remediation. The distinction between Pass and Merit in Part 1 is not whether the tools work — at Pass they mostly do. It is whether they are robust against unexpected input.

---

## Appendix A — Technical Specification & Field Test Contract

> Your code will be tested against an automated flow. If your scripts do not accept the specified arguments or produce output in the specified format, the tests will fail.

### Global Requirements

- Python 3.10+ only.
- **Never use `input()`** — it halts automation. All input comes through `argparse`. No exceptions.
- Do not shell out to external tools. Use native Python libraries.
- Scripts must exit with a non-zero return code on error and print error messages to `stderr`.

**Allowed non-standard libraries:**

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client (Task 4) |
| `paramiko` | SSH automation (Task 3) |
| `beautifulsoup4` | HTML parsing (Task 4) |

Additional libraries must be documented in `requirements.txt` and justified in `docs/build.md`.

### Tool Specifications

| Task | Title | Filename | CLI Arguments | Required Logic | Output Contract |
|------|-------|----------|---------------|----------------|-----------------|
| 1 — The Scene | The Evidence Collector | `log_parser.py` | `input_file` (positional); `--output` (default: `suspects.csv`) | Must use `re`. Match `"Failed password"` or `"Invalid user"`. | CSV: `Timestamp, IP_Address, User_Account` |
| 2 — The Map | The Network Cartographer | `scan.py` | `target` (IP); `--ports` (range or list) | `socket` only. Timeout 0.5s default. Banner `recv()` on open port. | JSON: `{"target":"...","open_ports":[{"port":21,"banner":"..."}]}` |
| 3 — The Key | The Access Validator | `brute.py` | `target`; `--service` (ssh\|ftp); `--user`; `--wordlist` | `paramiko` (SSH), `ftplib` (FTP). `time.sleep(0.1)` between every attempt. | `[+] SUCCESS: Password found: <password>` |
| 4 — The Surface | The Web Enumerator | `web_enum.py` | `url` (target URL) | `requests` + `bs4`. Extract `Server`, `X-Powered-By`. Extract all HTML comments. | `[HEADERS]`, `[COMMENTS]`, `[SENSITIVE PATHS]` sections. |

### Prohibited Functions

| Function | Reason |
|----------|--------|
| `input()` | Halts all automated testing. Use `argparse`. |
| `os.system()` / `subprocess.call()` | Do not wrap external tools. Use native Python libraries. |
| Metasploit (any form) | Prohibited in Part 2. Voids Mission submission. |

### Mission (Part 2) — Operational Rules

1. Submit the exact code used to retrieve the Flag. It must run in the lab environment without modification.
2. `requirements.txt` must be present and current.
3. Manual flag retrieval without a working script: Part 2 mark capped at Pass level.
4. `AI_LOG.md` must be committed before the session ends.
5. No commits after the session closes. GitHub Classroom timestamp is definitive.

---

*COM5413 — University of Bolton | 2025–26 | Module Leader: Beeteetoo
