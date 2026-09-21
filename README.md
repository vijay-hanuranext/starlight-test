# CRM Login Tests

Playwright + pytest test suite for CRM login.

## Setup

1. Install dependencies:
   ```
   uv venv
   .venv\Scripts\activate
   uv pip install -r requirements.txt
   playwright install
   ```

2. Create a `.env` file (copy `.env.example`) and fill in your credentials:
   ```
   BASE_URL=https://crm.hanuranext.com
   CRM_USERNAME=your_username
   CRM_PASSWORD=your_password
   ```

## Run tests

```
uv run pytest --headed --slowmo 300
```
