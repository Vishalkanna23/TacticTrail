
import json
from pathlib import Path

# Location of the extracted MITRE dataset
DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "enterprise_techniques.json"
)


def search_technique(technique_id):
    # Open the dataset
    with open(DATA_FILE, encoding="utf-8") as file:
        techniques = json.load(file)

    # Search for an exact technique ID
    for technique in techniques:
        if technique["technique_id"] == technique_id:
            return technique

    # No matching ID exists in our dataset
    return None


if __name__ == "__main__":
    user_id = input("Enter technique ID: ").strip().upper()

    result = search_technique(user_id)

    if result is not None:
        print("\nTechnique found!")
        print("ID:", result["technique_id"])
        print("Name:", result["name"])
        print("Tactics:", ", ".join(result["tactics"]))
        print("Description:", result["description"][:300])
        print("Source:", result["url"])
    else:
        print("Technique ID not found in the dataset.")
