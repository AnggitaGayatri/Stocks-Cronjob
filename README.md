# Automated Stock Data Downloader and Updater

This repository contains a GitHub Actions workflow that automatically downloads stock data from Yahoo Finance and updates it in a Firestore database. The workflow is scheduled to run at specific times during the weekdays (Monday to Friday) to ensure the stock data is up-to-date.

## Workflow Overview

The GitHub Actions workflow performs the following tasks:

1. **Download Stock Data:**
   - Retrieves stock data for companies listed in the LQ45 index using Yahoo Finance's API (via `yfinance` Python library).
   - Data is downloaded at an hourly interval.

2. **Update Firestore Database:**
   - The stock data is then stored in Firebase Firestore under the appropriate collections and documents.
   - The data is saved with fields such as: `Open`, `Close`, `High`, `Low`, `Volume`, and `Adj Close`.

3. **Schedule:**
   - The workflow is scheduled to run every weekday (Monday to Friday) at the following times:
     - 10:15 AM WITA
     - 11:15 AM WITA
     - 12:15 PM WITA
     - 2:15 PM WITA
     - 3:15 PM WITA
     - 4:15 PM WITA
     - 5:15 PM WITA
   - This is handled using a cron expression in GitHub Actions.

## Requirements

- **Firebase Project:**
  - You need a Firebase project and credentials (Service Account JSON) to connect to Firestore.
  - Store your Firebase credentials as GitHub Secrets (e.g., `FIREBASE_CREDENTIALS`).

- **Python Environment:**
  - The workflow uses Python 3 with the following dependencies:
    - `firebase-admin` - for interacting with Firebase Firestore.
    - `yfinance` - to download stock data.
    - `pandas` - for data manipulation.

## How the Workflow Works

1. **Trigger:**  
   The workflow is triggered automatically based on the schedule defined in the `.github/workflows` folder using the cron expression.

2. **Steps in the Workflow:**
   - Checkout the repository.
   - Set up the Python environment.
   - Install the necessary dependencies (`firebase-admin`, `yfinance`, `pandas`).
   - Set up Firebase using credentials from GitHub Secrets.
   - Download stock data for all companies in the LQ45 index.
   - Process and store the data in Firestore.

## Workflow File: `.github/workflows/stock_data_downloader.yml`

```yaml
name: Stock Data Downloader and Updater

on:
  schedule:
    - cron: '15 2,3,4,6,7,8,9 * * 1-5' # Runs every weekday at 10:15, 11:15, 12:15, 14:15, 15:15, 16:15, 17:15 WITA
  workflow_dispatch: # Allows manual trigger of the workflow

jobs:
  update-stock-data:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install Dependencies
      run: |
        pip install --upgrade pip
        pip install firebase-admin yfinance pandas

    - name: Set up Firebase Credentials
      run: echo "${{ secrets.FIREBASE_CREDENTIALS }}" > ./firebase_credentials.json

    - name: Run Stock Data Script
      run: |
        python /path/to/your/script/unduh_data.py
