# 10 real questions my user will ask

**Project:** TacticTrail (B-ENT-05)  
**User:** A security operations analyst at a bank  
**Knowledge source:** MITRE ATT&CK Enterprise  
**Purpose:** Initial evaluation questions for exact-ID lookup, multi-document retrieval, grounded answers, and safe abstention.

These questions are written in the style of an analyst investigating alerts. The incident scenarios are **hypothetical**, not claims about real bank events.

| # | Question | Where the answer is (document, page) | Needs more than one page? |
|---|---|---|---|
| 1 | An employee received a malicious Word document by email. Which ATT&CK technique matches it, and how is that different from a phishing email containing a malicious link? | MITRE ATT&CK: [T1566.001 – Spearphishing Attachment](https://attack.mitre.org/techniques/T1566/001/) and [T1566.002 – Spearphishing Link](https://attack.mitre.org/techniques/T1566/002/) | Yes |
| 2 | Our endpoint security tool detected suspicious access to LSASS process memory. Which exact ATT&CK sub-technique is this, and what mitigations or detection guidance does MITRE provide? | MITRE ATT&CK: [T1003.001 – LSASS Memory](https://attack.mitre.org/techniques/T1003/001/) (description, mitigations, detection strategy) | No |
| 3 | A Windows server has a suspicious scheduled task that runs after reboot. Which ATT&CK ID should we investigate, and which documented threat groups have used scheduled tasks for persistence? | MITRE ATT&CK: [T1053.005 – Scheduled Task](https://attack.mitre.org/techniques/T1053/005/) and [G0016 – APT29](https://attack.mitre.org/groups/G0016/) (one documented example; other groups may also apply) | Yes |
| 4 | An alert indicates an attacker executed malicious PowerShell commands. Which MITRE technique ID and tactic describe this behavior? | MITRE ATT&CK: [T1059.001 – PowerShell](https://attack.mitre.org/techniques/T1059/001/) | No |
| 5 | What is the ATT&CK difference between an attacker using PowerShell and using cmd.exe to run commands on Windows? Give both exact sub-technique IDs. | MITRE ATT&CK: [T1059.001 – PowerShell](https://attack.mitre.org/techniques/T1059/001/) and [T1059.003 – Windows Command Shell](https://attack.mitre.org/techniques/T1059/003/) | Yes |
| 6 | Our identity logs show someone trying the same common password against hundreds of accounts. Which ATT&CK sub-technique matches this? | MITRE ATT&CK: [T1110.003 – Password Spraying](https://attack.mitre.org/techniques/T1110/003/) | No |
| 7 | Several file shares became inaccessible after files were encrypted during a suspected ransomware incident. Which ATT&CK technique and tactic describe the encryption behavior? | MITRE ATT&CK: [T1486 – Data Encrypted for Impact](https://attack.mitre.org/techniques/T1486/) | No |
| 8 | An attacker used a stolen employee account to log into another Windows machine over Remote Desktop. Which ATT&CK techniques cover the account abuse and the remote access? | MITRE ATT&CK: [T1078 – Valid Accounts](https://attack.mitre.org/techniques/T1078/) and [T1021.001 – Remote Desktop Protocol](https://attack.mitre.org/techniques/T1021/001/) | Yes |
| 9 | Our public-facing customer portal was exploited to obtain an initial foothold. Which ATT&CK technique should the SOC investigate first? | MITRE ATT&CK: [T1190 – Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/) | No |
| 10 | How many confirmed phishing incidents occurred in our bank's retail business unit last month? | **None in the MITRE ATT&CK knowledge base.** Requires authorized, tenant-specific internal incident records. | No — cannot be answered from these documents |

## Expected answer IDs (initial evaluation key)

| Question | Expected technique ID(s) or behavior |
|---|---|
| 1 | `T1566.001` and `T1566.002`; distinguish attachment from link |
| 2 | `T1003.001`; cite the official record for any mitigation/detection claims |
| 3 | `T1053.005`; cite a documented group such as `G0016` (APT29) |
| 4 | `T1059.001` (PowerShell; Execution) |
| 5 | `T1059.001` and `T1059.003` |
| 6 | `T1110.003` (Password Spraying) |
| 7 | `T1486` (Data Encrypted for Impact; Impact) |
| 8 | `T1078` and `T1021.001` |
| 9 | `T1190` (Exploit Public-Facing Application) |
| 10 | Abstain: explain MITRE does not contain this bank's private incident counts; do not invent a number |

## Evaluation notes

- Questions **1, 3, 5, and 8** require evidence from more than one ATT&CK page.
- Question **10** intentionally tests whether the assistant refuses to fabricate unsupported internal information.
- The initial local extraction contains **Enterprise attack techniques only**. Group relationships, full mitigations/detections, and tenant-specific incident data are **future ingestion features**; do not mark those functions as implemented yet.
- These are **10 starter questions**, not the college's complete **100-query benchmark**. The final goal is the correct technique ID in the top three results for at least 92 of 100 evaluation queries, with zero invented IDs.
- Answers should provide exact technique IDs, tactic(s), and official source links. Scenarios alone are not proof that an attack occurred.
