import os
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

print("=" * 70)
print("FIFA WORLD CUP 2026 SCRAPER")
print("=" * 70)

# ============================================================
# URLs
# ============================================================

TEAM_URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/team-statistics"

PLAYER_URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"

# ============================================================
# Output folders
# ============================================================

TEAM_FOLDER = "data/raw/fifa/team_stats"
PLAYER_FOLDER = "data/raw/fifa/player_stats"

os.makedirs(TEAM_FOLDER, exist_ok=True)
os.makedirs(PLAYER_FOLDER, exist_ok=True)

# ============================================================
# Tabs
# ============================================================

TEAM_TABS = [
    "Attacking",
    "Distribution",
    "Defending",
    "Discipline",
    "Goalkeeping",
    "Movement",
    "Physical"
]

PLAYER_TABS = [
    "adidas Golden Boot",
    "Attacking",
    "Distribution",
    "Defending",
    "Discipline",
    "Goalkeeping",
    "Movement",
    "Physical"
]

# ============================================================
# Browser
# ============================================================

def start_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page = browser.new_page(
        viewport={
            "width": 1700,
            "height": 950
        }
    )

    page.set_default_timeout(60000)

    return playwright, browser, page

# ============================================================
# Open Page
# ============================================================

def open_page(page, url):

    print("\nOpening")
    print(url)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=120000
    )

    page.wait_for_timeout(5000)

    # remove cookie overlays
    page.evaluate("""
    () => {

        document.querySelectorAll(
            "#onetrust-consent-sdk"
        ).forEach(e=>e.remove());

        document.querySelectorAll(
            ".onetrust-pc-dark-filter"
        ).forEach(e=>e.remove());

        document.querySelectorAll(
            ".onetrust-pc-sdk"
        ).forEach(e=>e.remove());

        document.body.style.overflow="auto";

    }
    """)

# ============================================================
# Click Tab
# ============================================================

def click_tab(page,name):

    print(f"\nOpening {name}")

    locator = page.get_by_role(
        "button",
        name=name,
        exact=True
    )

    locator.scroll_into_view_if_needed()

    locator.click(force=True)

    page.wait_for_timeout(5000)

# ============================================================
# Save CSV
# ============================================================

def save_csv(df,folder,name):

    filename = (
        name
        .lower()
        .replace(" ","_")
        .replace("-","_")
    )

    path = os.path.join(
        folder,
        filename + ".csv"
    )

    df.to_csv(
        path,
        index=False
    )

    print(f"Saved -> {path}")

# ============================================================
# Extract HTML Table
# ============================================================

def extract_table(page):

    print("Waiting for statistics table...")

    # Wait until at least one row exists
    page.locator("tbody tr").first.wait_for(timeout=60000)

    page.wait_for_timeout(3000)

    html = page.content()

    # Save HTML for debugging
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "lxml")

    tables = soup.find_all("table")

    print(f"Tables Found : {len(tables)}")

    if len(tables) == 0:
        return None

    table = tables[0]

    headers = []

    thead = table.find("thead")

    if thead:

        for th in thead.find_all("th"):

            text = th.get_text(" ", strip=True)

            if text == "":
                text = f"Column_{len(headers)+1}"

            headers.append(text)

    rows = []

    tbody = table.find("tbody")

    if tbody:

        for tr in tbody.find_all("tr"):

            row = []

            for td in tr.find_all("td"):

                text = td.get_text(" ", strip=True)

                row.append(text)

            rows.append(row)

    if len(rows) == 0:

        print("No rows found.")

        return None

    # Auto-create headers if FIFA doesn't provide them
    if len(headers) == 0:

        headers = [

            f"Column_{i+1}"

            for i in range(len(rows[0]))

        ]

    # Match header count with row count
    if len(headers) != len(rows[0]):

        headers = [

            f"Column_{i+1}"

            for i in range(len(rows[0]))

        ]

    df = pd.DataFrame(rows, columns=headers)

    print(df.head())

    return df


# ============================================================
# Team Statistics
# ============================================================

def scrape_team_statistics(page):

    print("\n")
    print("=" * 70)
    print("TEAM STATISTICS")
    print("=" * 70)

    open_page(page, TEAM_URL)

    # -------------------------------------------------------

    # First tab (already selected)

    print("\nDownloading Attacking")

    df = extract_table(page)

    if df is not None:

        save_csv(

            df,

            TEAM_FOLDER,

            "attacking"

        )

    else:

        print("Attacking failed.")

    # -------------------------------------------------------

    for tab in TEAM_TABS[1:]:

        print("\n")
        print("=" * 60)

        print(tab)

        try:

            click_tab(page, tab)

            df = extract_table(page)

            if df is None:

                print("Table Missing")

                continue

            save_csv(

                df,

                TEAM_FOLDER,

                tab

            )

        except Exception as e:

            print(e)

            continue

    print("\nTeam Statistics Completed")

# ============================================================
# PLAYER STATISTICS
# ============================================================

def scrape_player_statistics(page):

    print("\n")
    print("=" * 70)
    print("PLAYER STATISTICS")
    print("=" * 70)

    open_page(page, PLAYER_URL)

    # -------------------------------------------------------
    # First tab (already selected)
    # -------------------------------------------------------

    print("\nDownloading adidas Golden Boot")

    df = extract_table(page)

    if df is not None:

        save_csv(
            df,
            PLAYER_FOLDER,
            "golden_boot"
        )

    else:

        print("Golden Boot table not found.")

    # -------------------------------------------------------
    # Remaining Tabs
    # -------------------------------------------------------

    for tab in PLAYER_TABS[1:]:

        print("\n")
        print("=" * 60)
        print(f"Downloading {tab}")

        try:

            click_tab(page, tab)

            df = extract_table(page)

            if df is None:

                print(f"{tab} skipped.")
                continue

            save_csv(
                df,
                PLAYER_FOLDER,
                tab
            )

        except Exception as e:

            print(f"Error in {tab}")
            print(e)

            continue

    print("\nPlayer Statistics Completed")


# ============================================================
# VERIFY CSV FILES
# ============================================================

def verify_downloads():

    print("\n")
    print("=" * 70)
    print("VERIFYING DOWNLOADS")
    print("=" * 70)

    print("\nTEAM FILES")

    if os.path.exists(TEAM_FOLDER):

        for file in sorted(os.listdir(TEAM_FOLDER)):

            if file.endswith(".csv"):

                print("✓", file)

    print("\nPLAYER FILES")

    if os.path.exists(PLAYER_FOLDER):

        for file in sorted(os.listdir(PLAYER_FOLDER)):

            if file.endswith(".csv"):

                print("✓", file)


# ============================================================
# CLEAN DATAFRAME
# ============================================================

def clean_dataframe(df):

    if df is None:
        return None

    df.columns = [

        re.sub(r"\s+", "_", str(col).strip().lower())

        for col in df.columns

    ]

    df = df.drop_duplicates()

    df = df.reset_index(drop=True)

    return df


# ============================================================
# SAVE CLEAN CSV
# ============================================================

def save_clean_csv(df, folder, filename):

    if df is None:
        return

    df = clean_dataframe(df)

    path = os.path.join(folder, filename + ".csv")

    df.to_csv(path, index=False)

    print(f"Saved -> {path}")