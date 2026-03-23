# Google Drive Sync Setup Guide

## 1. Google Cloud Setup

### Create a Project and Enable APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable these APIs:
   - Google Drive API
   - Google Docs API

### Create a Service Account

1. Navigate to IAM & Admin → Service Accounts
2. Click "Create Service Account"
3. Name: `easydoctor-specs-sync`
4. Grant role: none (will use Drive sharing instead)
5. Create and download JSON key
6. Move the file to **`config/credentials/gdrive-service-account.json`** (canonical path; matches `GDRIVE_SERVICE_ACCOUNT_PATH` in `.env.sample`). You may download to `tmp/` first, then `mv` — never commit the JSON.

### Configure Drive Folder Sharing

1. Create a folder in Google Drive: "EasyDoctor Specs"
2. Share it with the service account email (from the JSON key): give "Editor" access
3. Copy the folder ID from the URL: `https://drive.google.com/drive/folders/<FOLDER_ID>`

## 2. Store Credentials Securely

For local development, store paths in `.env` (gitignored):
```bash
GDRIVE_SERVICE_ACCOUNT_PATH=config/credentials/gdrive-service-account.json
GDRIVE_SPECS_FOLDER_ID=your-folder-id-here
```

Add to `.env.sample`:
```bash
GDRIVE_SPECS_FOLDER_ID=your-google-drive-folder-id
GDRIVE_SERVICE_ACCOUNT_PATH=config/credentials/gdrive-service-account.json
```

## 3. Add Required Python Packages

Install with pip:
```bash
pip install google-api-python-client google-auth google-auth-httplib2 markdown
```

## 4. Script Installation

The scripts in `.cursor/skills/gdrive-specs-sync/scripts/` are standalone Python scripts.
They use the packages above.

Make them executable:
```bash
chmod +x .cursor/skills/gdrive-specs-sync/scripts/publish_spec.py
chmod +x .cursor/skills/gdrive-specs-sync/scripts/fetch_comments.py
```

## 5. Test the Connection

```bash
# Test authentication
python -c "
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
creds = service_account.Credentials.from_service_account_file(
    os.environ['GDRIVE_SERVICE_ACCOUNT_PATH'],
    scopes=['https://www.googleapis.com/auth/drive']
)
service = build('drive', 'v3', credentials=creds)
folder_id = os.environ['GDRIVE_SPECS_FOLDER_ID']
files = service.files().list(q=f\"'{folder_id}' in parents\", pageSize=10).execute()
print('Connection successful! Files:', [f['name'] for f in files.get('files', [])])
"
```

## 6. Sharing with Stakeholders

The `publish_spec.py` script accepts a `--share` flag:

```bash
python .cursor/skills/gdrive-specs-sync/scripts/publish_spec.py \
  specs/features/my-feature.md \
  --share stakeholder@example.com,other@example.com
```

This sets `reader` permission for the specified emails on the uploaded document.

## Security Notes

- The service account JSON key must NEVER be committed to git
- Add `config/credentials/gdrive-service-account.json` to `.gitignore`
- In production/CI, use environment variables or encrypted credentials
- The service account only has access to the explicitly shared folder, not the entire Drive
