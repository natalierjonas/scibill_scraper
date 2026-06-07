{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "4901ac45",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: playwright in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (1.56.0)\n",
      "Requirement already satisfied: beautifulsoup4 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (4.14.2)\n",
      "Requirement already satisfied: pandas in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (2.3.3)\n",
      "Requirement already satisfied: tqdm in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (4.67.1)\n",
      "Requirement already satisfied: pyee<14,>=13 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from playwright) (13.0.0)\n",
      "Requirement already satisfied: greenlet<4.0.0,>=3.1.1 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from playwright) (3.2.4)\n",
      "Requirement already satisfied: typing-extensions in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from pyee<14,>=13->playwright) (4.15.0)\n",
      "Requirement already satisfied: soupsieve>1.2 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from beautifulsoup4) (2.8)\n",
      "Requirement already satisfied: numpy>=1.26.0 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from pandas) (2.3.4)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from pandas) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Requirement already satisfied: six>=1.5 in /Users/nataliejonas/.pyenv/versions/3.13.9/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
      "\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.3\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.1.2\u001b[0m\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpip install --upgrade pip\u001b[0m\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "%pip install playwright beautifulsoup4 pandas tqdm\n",
    "!playwright install firefox"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "0257e337",
   "metadata": {},
   "outputs": [],
   "source": [
    "import asyncio\n",
    "import pandas as pd\n",
    "import re\n",
    "from bs4 import BeautifulSoup\n",
    "from playwright.async_api import async_playwright\n",
    "\n",
    "BASE_URL = \"https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22type%22%3A%22bills%22%2C%22house-committee%22%3A%22Science%2C+Space%2C+and+Technology%22%7D\"\n",
    "\n",
    "OUTPUT_FILE = \"bills.csv\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "8df69ccd",
   "metadata": {},
   "outputs": [],
   "source": [
    "def parse_sponsor(text):\n",
    "    if not text:\n",
    "        return {}\n",
    "\n",
    "    name_match = re.search(r\"Sponsor:\\s*(.*?)\\s*\\[\", text)\n",
    "    party_match = re.search(r\"\\[Rep\\.-(R|D|I)-([A-Z]{2})-(\\d+)\\]\", text)\n",
    "    cosponsors_match = re.search(r\"Cosponsors:\\s*\\(\\s*(\\d+)\\s*\\)\", text)\n",
    "    date_match = re.search(r\"\\(Introduced\\s*([0-9/]+)\\)\", text)\n",
    "\n",
    "    return {\n",
    "        \"sponsor_name\": name_match.group(1).strip() if name_match else None,\n",
    "        \"party\": party_match.group(1) if party_match else None,\n",
    "        \"state\": party_match.group(2) if party_match else None,\n",
    "        \"district\": party_match.group(3) if party_match else None,\n",
    "        \"cosponsors\": int(cosponsors_match.group(1)) if cosponsors_match else 0,\n",
    "        \"introduced_date\": date_match.group(1) if date_match else None,\n",
    "    }\n",
    "\n",
    "\n",
    "def clean_status(text):\n",
    "    if not text:\n",
    "        return None\n",
    "    return text.split(\"Array\")[0].strip()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "d5efa6c3",
   "metadata": {},
   "outputs": [],
   "source": [
    "def parse_bill(li):\n",
    "    heading = li.select_one(\"span.result-heading a\")\n",
    "    bill_number = heading.get_text(strip=True) if heading else None\n",
    "    bill_url = \"https://www.congress.gov\" + heading[\"href\"] if heading else None\n",
    "\n",
    "    title = li.select_one(\"span.result-title\")\n",
    "    title = title.get_text(\" \", strip=True) if title else None\n",
    "\n",
    "    sponsor_raw = None\n",
    "    committees = None\n",
    "    latest_action = None\n",
    "\n",
    "    for item in li.select(\"span.result-item\"):\n",
    "        txt = item.get_text(\" \", strip=True)\n",
    "        if \"Sponsor:\" in txt:\n",
    "            sponsor_raw = txt\n",
    "        elif \"Committees:\" in txt:\n",
    "            committees = txt\n",
    "        elif \"Latest Action:\" in txt:\n",
    "            latest_action = txt\n",
    "\n",
    "    status_el = li.select_one(\"ol.stat_leg li.selected\")\n",
    "    status = clean_status(status_el.get_text(\" \", strip=True) if status_el else None)\n",
    "\n",
    "    sponsor_data = parse_sponsor(sponsor_raw)\n",
    "\n",
    "    return {\n",
    "        \"bill_number\": bill_number,\n",
    "        \"bill_url\": bill_url,\n",
    "        \"title\": title,\n",
    "        \"committees\": committees,\n",
    "        \"latest_action\": latest_action,\n",
    "        \"status\": status,\n",
    "        **sponsor_data,\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "f068bcd3",
   "metadata": {},
   "outputs": [],
   "source": [
    "async def scrape_all():\n",
    "    all_data = []\n",
    "    page_num = 1\n",
    "\n",
    "    async with async_playwright() as p:\n",
    "        browser = await p.firefox.launch(headless=False)\n",
    "        page = await browser.new_page()\n",
    "\n",
    "        while True:\n",
    "            url = BASE_URL + f\"&page={page_num}\"\n",
    "            print(f\"Scraping page {page_num}...\")\n",
    "\n",
    "            await page.goto(url, wait_until=\"networkidle\", timeout=120000)\n",
    "\n",
    "            soup = BeautifulSoup(await page.content(), \"html.parser\")\n",
    "            bills = soup.select(\"li.expanded\")\n",
    "\n",
    "            if len(bills) == 0:\n",
    "                print(\"No more results. stopping.\")\n",
    "                break\n",
    "\n",
    "            for b in bills:\n",
    "                all_data.append(parse_bill(b))\n",
    "\n",
    "            print(f\"  → {len(bills)} bills (total {len(all_data)})\")\n",
    "\n",
    "            page_num += 1\n",
    "\n",
    "        await browser.close()\n",
    "\n",
    "    return all_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "e004ecda",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Scraping page 1...\n",
      "  → 100 bills (total 100)\n",
      "Scraping page 2...\n",
      "  → 100 bills (total 200)\n",
      "Scraping page 3...\n",
      "No more results. stopping.\n",
      "Total scraped: 200\n",
      "{'bill_number': 'H.R.9154', 'bill_url': 'https://www.congress.gov/bill/119th-congress/house-bill/9154?s=1&r=1', 'title': 'To direct the Secretary of Commerce to develop a methodology for identifying country of origin of shrimp, and for other purposes.', 'committees': 'Committees: House - Natural Resources; Science, Space, and Technology', 'latest_action': 'Latest Action: House - 06/04/2026 Referred to the Committee on Natural Resources, and in addition to the Committee on Science, Space, and Technology , for a period to be subsequently determined by the Speaker, in each case for consideration of such provisions as fall within the jurisdiction of the... ( All Actions )', 'status': 'Introduced', 'sponsor_name': 'Mace, Nancy', 'party': 'R', 'state': 'SC', 'district': '1', 'cosponsors': 3, 'introduced_date': '06/04/2026'}\n"
     ]
    }
   ],
   "source": [
    "data = await scrape_all()\n",
    "\n",
    "print(\"Total scraped:\", len(data))\n",
    "print(data[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "fc420079",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Saved 200 total rows to bills.csv\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "\n",
    "df_new = pd.DataFrame(data)\n",
    "\n",
    "# Load existing file if it exists\n",
    "if os.path.exists(OUTPUT_FILE):\n",
    "    df_old = pd.read_csv(OUTPUT_FILE)\n",
    "\n",
    "    # append-only (no dedup logic required)\n",
    "    df_final = pd.concat([df_old, df_new], ignore_index=True)\n",
    "else:\n",
    "    df_final = df_new\n",
    "\n",
    "df_final.to_csv(OUTPUT_FILE, index=False)\n",
    "\n",
    "print(f\"Saved {len(df_final)} total rows to {OUTPUT_FILE}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "3.13.9",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
