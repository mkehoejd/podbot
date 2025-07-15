# details_extractor.py

import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import os

# Extract contact info from a URL
def extract_contact_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "N/A", "N/A"

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Find emails and phone numbers
        emails = list(set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)))
        phones = list(set(re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)))

        # Clean and format
        clean_emails = [email.strip().lower() for email in emails if "@" in email]
        clean_phones = [re.sub(r"[^\d]", "", phone) for phone in phones if len(re.sub(r"[^\d]", "", phone)) >= 10]
        formatted_phones = [f"+1 ({p[:3]}) {p[3:6]}-{p[6:]}" for p in clean_phones]

        return ", ".join(clean_emails), ", ".join(formatted_phones)

    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return "N/A", "N/A"

# Enrich CSV with scraped emails and phones
def enrich_csv(csv_path):
    df = pd.read_csv(csv_path)
    df["Email(s)"] = ""
    df["Phone(s)"] = ""

    for index, row in df.iterrows():
        url = row.get("link", "")
        if url and url.startswith("http"):
            print(f"🔗 Scraping {url}")
            emails, phones = extract_contact_info(url)
            df.at[index, "Email(s)"] = emails
            df.at[index, "Phone(s)"] = phones

    df.to_csv(csv_path, index=False)
    print(f"✅ Enriched and saved: {csv_path}")
    append_to_master(csv_path)

# Append enriched leads to a master file without duplicates
def append_to_master(enriched_csv_path, master_csv_path="leads/outdoor_master_list.csv"):
    new_data = pd.read_csv(enriched_csv_path)

    if not os.path.exists(master_csv_path):
        new_data.to_csv(master_csv_path, index=False)
        print(f"🧱 Master list created at {master_csv_path}")
        return

    master_data = pd.read_csv(master_csv_path)

    combined = pd.concat([master_data, new_data], ignore_index=True)
    combined.drop_duplicates(subset=["link"], inplace=True)  # dedupe on link (edit if needed)

    combined.to_csv(master_csv_path, index=False)
    print(f"📈 Master list updated: {len(combined)} total entries")