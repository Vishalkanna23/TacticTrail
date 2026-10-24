
import json
from pathlib import Path

# Original MITRE ATT&CK dataset
source = Path("data/raw/enterprise-attack-20.0.json")

# Check that the file exists
if not source.exists():
    raise SystemExit("MITRE dataset not found in data/raw/")

# Read the JSON file
with source.open("r", encoding="utf-8") as file:
    data = json.load(file)

techniques = []

# Examine each STIX object
for item in data["objects"]:

    # Keep only active attack techniques
    if item.get("type") != "attack-pattern":
        continue

    if item.get("revoked") or item.get("x_mitre_deprecated"):
        continue

    # Find the official MITRE technique ID
    mitre_ref = None

    for ref in item.get("external_references", []):
        if (
            ref.get("source_name") == "mitre-attack"
            and ref.get("external_id", "").startswith("T")
        ):
            mitre_ref = ref
            break

    if mitre_ref is None:
        continue

    # Extract the tactics
    tactics = []
    for phase in item.get("kill_chain_phases", []):
        if phase.get("kill_chain_name") == "mitre-attack":
            tactic = phase["phase_name"].replace("-", " ").title()
            if tactic not in tactics:
                tactics.append(tactic)

    technique = {
        "technique_id": mitre_ref["external_id"],
        "name": item.get("name", ""),
        "description": item.get("description", ""),
        "tactics": tactics,
        "is_subtechnique": item.get("x_mitre_is_subtechnique", False),
        "url": mitre_ref.get("url", ""),
        "stix_id": item["id"],
    }

    techniques.append(technique)

# Sort by technique ID
techniques.sort(key=lambda item: item["technique_id"])

# Save the extracted data
output = Path("data/raw/enterprise_techniques.json")
output.write_text(
    json.dumps(techniques, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

# Save 10 example records in our GitHub sample folder
sample = Path("data/sample/techniques_sample.json")
sample.parent.mkdir(parents=True, exist_ok=True)
sample.write_text(
    json.dumps(techniques[:10], indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("Total STIX objects:", len(data["objects"]))
print("Active techniques extracted:", len(techniques))
print("Sample records saved:", min(10, len(techniques)))

if techniques:
    print("Example:", techniques[0]["technique_id"], techniques[0]["name"])
