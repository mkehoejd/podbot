from search_google import search_outdoor_companies
from datetime import datetime
import pandas as pd
import os
import details_extractor
import random
import socket
from pathlib import Path

LOCKFILE = Path("leads/.scraper_lock")

def already_ran_today():
    if LOCKFILE.exists():
        modified = datetime.fromtimestamp(LOCKFILE.stat().st_mtime)
        return modified.date() == datetime.now().date()
    return False

def write_lock():
    LOCKFILE.touch()

# Generic search terms
SEARCH_TERMS = [
    "fly fishing guides", "hunting outfitters", "archery shops", "outdoor gear stores",
    "ATV rentals", "horseback trail rides", "backcountry guides", "camping equipment stores",
    "whitewater rafting companies", "ski and snowboard shops", "mountain biking tours",
    "climbing gyms", "survival training schools", "gun shops", "conservation nonprofits",
    "elk hunting guides", "national park tours", "guided wildlife photography tours",
    "outdoor education programs", "dude ranches", "trapshooting clubs", "upland bird guides",
    "shed hunting outfitters", "custom knife makers", "outdoor apparel companies",
    "river shuttle services", "offroad vehicle rental", "backpacking guides", "glamping companies",
    "wildlife biologists", "ornithologists", "avian researchers", "bird watching clubs",
    "birding societies", "wildlife conservancy", "ecological consulting", "habitat restoration",
    "wildlife rehab centers", "forest ecology research", "bird banding stations",
    "wildlife tracking organizations"
]

# Global location pool
LOCATIONS = [
    "United States", "Canada", "Australia", "New Zealand", "United Kingdom", "Ireland",
    "South Africa", "Brazil", "Netherlands", "Sweden", "Norway", "Finland", "Germany",
    "Switzerland", "Austria"
]

def internet_available(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def main():
    random.seed(datetime.now().strftime("%Y%m%d"))
    term = random.choice(SEARCH_TERMS)
    location = random.choice(LOCATIONS)

    slug_term = term.replace(" ", "_")
    slug_loc = location.replace(" ", "_")
    filename = f"leads/outdoor_leads_{slug_term}_{slug_loc}_{datetime.now().strftime('%Y-%m-%d')}.csv"

    print(f"🔍 Searching for '{term}' in '{location}'")
    results = search_outdoor_companies(term, location)

    if not results:
        print("⚠️ No results found.")
        return

    os.makedirs("leads", exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    details_extractor.enrich_csv(filename)

    print(f"✅ Leads saved to {filename}")

if __name__ == "__main__":
    main()