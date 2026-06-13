import asyncio
import os
import pandas as pd

import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

BASE_URL = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22type%22%3A%22bills%22%2C%22house-committee%22%3A%22Science%2C+Space%2C+and+Technology%22%7D"

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bills.csv")

def parse_sponsor(text):
    if not text:
        return {}

    name_match = re.search(r"Sponsor:\s*(.*?)\s*\[", text)
    party_match = re.search(r"\[Rep\.-(R|D|I)-([A-Z]{2})-(\d+)\]", text)
    cosponsors_match = re.search(r"Cosponsors:\s*\(\s*(\d+)\s*\)", text)
    date_match = re.search(r"\(Introduced\s*([0-9/]+)\)", text)

    return {
        "sponsor_name": name_match.group(1).strip() if name_match else None,
        "party": party_match.group(1) if party_match else None,
        "state": party_match.group(2) if party_match else None,
        "district": party_match.group(3) if party_match else None,
        "cosponsors": int(cosponsors_match.group(1)) if cosponsors_match else 0,
        "introduced_date": date_match.group(1) if date_match else None,
    }


def clean_status(text):
    if not text:
        return None
    return text.split("Array")[0].strip()

def parse_bill(li):
    heading = li.select_one("span.result-heading a")
    bill_number = heading.get_text(strip=True) if heading else None
    bill_url = "https://www.congress.gov" + heading["href"] if heading else None

    title = li.select_one("span.result-title")
    title = title.get_text(" ", strip=True) if title else None

    sponsor_raw = None
    committees = None
    latest_action = None

    for item in li.select("span.result-item"):
        txt = item.get_text(" ", strip=True)
        if "Sponsor:" in txt:
            sponsor_raw = txt
        elif "Committees:" in txt:
            committees = txt
        elif "Latest Action:" in txt:
            latest_action = txt

    status_el = li.select_one("ol.stat_leg li.selected")
    status = clean_status(status_el.get_text(" ", strip=True) if status_el else None)

    sponsor_data = parse_sponsor(sponsor_raw)

    return {
        "bill_number": bill_number,
        "bill_url": bill_url,
        "title": title,
        "committees": committees,
        "latest_action": latest_action,
        "status": status,
        **sponsor_data,
    }

import math

async def scrape_all(known_bills=None):
    """
    Full scrape when known_bills is empty (no CSV yet).
    Incremental scrape when known_bills is provided — stops as soon as a
    known bill number appears, since results are sorted newest-first.
    """
    if known_bills is None:
        known_bills = set()

    incremental = len(known_bills) > 0
    all_data = []
    seen_on_this_run = set()
    page_num = 1
    max_pages = None

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        while True:
            url = BASE_URL + f"&page={page_num}"
            label = f"page {page_num}" + (f"/{max_pages}" if max_pages else "")
            mode = "incremental" if incremental else "full"
            print(f"[{mode}] Scraping {label}...")

            await page.goto(url, wait_until="networkidle", timeout=120000)
            soup = BeautifulSoup(await page.content(), "html.parser")

            # Parse total on page 1 so we know the ceiling
            if page_num == 1:
                results_el = soup.select_one(".results-number")
                if results_el:
                    m = re.search(r"of\s*([\d,]+)", results_el.get_text(" ", strip=True))
                    if m:
                        total = int(m.group(1).replace(",", ""))
                        per_page = len(soup.select("li.expanded")) or 100
                        max_pages = math.ceil(total / per_page)
                        print(f"  Total results: {total} → {max_pages} pages")

            bills = soup.select("li.expanded")

            if not bills:
                print("No bills on this page. Stopping.")
                break

            new_count = 0
            reached_known = False
            for b in bills:
                parsed = parse_bill(b)
                bn = parsed.get("bill_number")
                if not bn:
                    continue
                if bn in known_bills:
                    # First bill we've seen before — everything after is older, already stored
                    reached_known = True
                    break
                if bn not in seen_on_this_run:
                    seen_on_this_run.add(bn)
                    all_data.append(parsed)
                    new_count += 1

            print(f"  → {new_count} new bills (total so far: {len(all_data)})")

            if reached_known:
                print("Caught up to existing data. Stopping.")
                break

            if new_count == 0:
                print("No new bills — likely looped. Stopping.")
                break

            # Primary stop: last page has no "Next Page" link
            if not soup.select_one("a.next"):
                print("No next-page link. Done.")
                break

            # Safety stop: never exceed calculated ceiling
            if max_pages and page_num >= max_pages:
                print(f"Reached final page ({max_pages}). Done.")
                break

            page_num += 1

        await browser.close()

    return all_data


def main():
    # Load existing bill numbers to drive incremental mode
    known_bills = set()
    if os.path.exists(OUTPUT_FILE):
        df_existing = pd.read_csv(OUTPUT_FILE)
        known_bills = set(df_existing["bill_number"].dropna().astype(str))
        print(f"Incremental mode: {len(known_bills)} existing bills loaded from {OUTPUT_FILE}")
    else:
        print("Full scrape mode: no existing CSV found")

    data = asyncio.run(scrape_all(known_bills=known_bills))
    print(f"\nNew bills scraped: {len(data)}")
    if data:
        print(data[0])

    # Alert check — raise so GitHub Actions marks the job failed and emails the owner
    if not data and not known_bills:
        raise RuntimeError(
            "Full scrape returned 0 bills. "
            "congress.gov may be blocking requests or the page structure has changed."
        )
    elif not data:
        print("No new bills since last run — nothing to add.")
        return

    print(f"OK: {len(data)} new bill(s) to save.")

    df_new = pd.DataFrame(data)

    if os.path.exists(OUTPUT_FILE):
        df_old = pd.read_csv(OUTPUT_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=["bill_number"], keep="last")
    else:
        df_final = df_new

    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df_final)} total rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()