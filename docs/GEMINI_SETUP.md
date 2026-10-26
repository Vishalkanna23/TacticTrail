# TacticTrail - Gemini AI Integration

## Overview
TacticTrail uses the Google Gemini API to generate
cybersecurity explanations from retrieved MITRE
ATT&CK evidence.

## Implementation
- Created app/gemini_service.py
- Created scripts/test_gemini.py
- Configured GEMINI_API_KEY using environment variables
- Used python-dotenv to load local configuration
- Added instructions to prevent invented MITRE IDs

## Testing
The initial integration reached the Gemini API.

Encountered:
- 404: The original model was unavailable.
- 503: The replacement model experienced high demand.

The first successful generated response is pending.

## Security
- API keys are stored in .env
- API keys must never be committed to GitHub
- Generated answers must be checked against MITRE records

## Next Steps
- Select a suitable available Gemini model
- Complete a successful generation test
- Connect Gemini to the FastAPI backend
- Add automated tests and usage tracking