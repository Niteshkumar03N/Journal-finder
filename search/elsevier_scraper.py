from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from urllib.parse import quote_plus

import re
import time

from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("ELSEVIER_URL")

# =====================================
# SEARCH FUNCTION
# =====================================

def search_elsevier(abstract):

    encoded_query = quote_plus(
        abstract
    )

    url = (
        f"{BASE_URL}"
        f"?goldOpenAccess=true"
        f"&subscription=true"
        f"&sortBy=default"
        f"&sortOrder=desc"
        f"&query={encoded_query}"
        f"&mode=recommend-stem"
        f"&ecrId="
        f"&agreementsFilter=all-journals"
    )

    # =====================================
    # CHROME OPTIONS
    # =====================================

    options = Options()

    options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--no-sandbox")

    # options.add_argument("--headless")

    # =====================================
    # OPEN BROWSER
    # =====================================

    driver = webdriver.Chrome(
        options=options
    )

    driver.get(url)

    # =====================================
    # WAIT FOR RESULTS
    # =====================================

    time.sleep(10)

    # =====================================
    # FIND RESULT CARDS
    # =====================================

    cards = driver.find_elements(
        By.TAG_NAME,
        "article"
    )

    all_journals = []

    # =====================================
    # LOOP THROUGH RESULTS
    # =====================================

    for card in cards:

        try:

            detail_text = (
                card.text
                .strip()
            )

            # =====================================
            # TITLE
            # =====================================

            title = "N/A"

            try:

                title = (
                    card.find_element(
                        By.TAG_NAME,
                        "h2"
                    )
                    .text
                    .strip()
                )

            except:
                pass

            # =====================================
            # JOURNAL URL
            # =====================================

            journal_url = ""

            try:

                links = card.find_elements(
                    By.TAG_NAME,
                    "a"
                )

                for a in links:

                    href = (
                        a.get_attribute(
                            "href"
                        )
                    )

                    if not href:
                        continue

                    if (
                        "journal"
                        in href.lower()
                        or
                        "sciencedirect"
                        in href.lower()
                        or
                        "elsevier"
                        in href.lower()
                    ):

                        journal_url = href
                        break

            except:
                pass

            # =====================================
            # IMPACT FACTOR
            # =====================================

            impact_factor = "—"

            impact_match = re.search(
                r'Impact\s*Factor\s*([\d.]+)',
                detail_text,
                re.IGNORECASE
            )

            if impact_match:

                impact_factor = (
                    impact_match.group(1)
                )

            # =====================================
            # CITESCORE
            # =====================================

            citescore = ""

            citescore_match = re.search(
                r'CiteScore\s*([\d.]+)',
                detail_text,
                re.IGNORECASE
            )

            if citescore_match:

                citescore = (
                    citescore_match.group(1)
                )

            # =====================================
            # SUBMISSION TO FIRST DECISION
            # =====================================

            first_decision = ""

            decision_match = re.search(
                r'Submission\s*to\s*first\s*decision\s*([\d]+\s*days)',
                detail_text,
                re.IGNORECASE
            )

            if decision_match:

                first_decision = (
                    decision_match.group(1)
                )

            # =====================================
            # ACCEPTANCE TO PUBLICATION
            # =====================================

            acceptance_to_publication = ""

            acceptance_match = re.search(
                r'Acceptance\s*to\s*publication\s*([\d]+\s*days)',
                detail_text,
                re.IGNORECASE
            )

            if acceptance_match:

                acceptance_to_publication = (
                    acceptance_match.group(1)
                )

            # =====================================
            # PUBLICATION CHARGE
            # =====================================

            publication_charge = ""

            publication_match = re.search(
                r'(\$[\d,]+)\s*Article\s*Publishing\s*Charge',
                detail_text,
                re.IGNORECASE
            )

            if publication_match:

                publication_charge = (
                    publication_match.group(1)
                )

            # =====================================
            # OPEN ACCESS / SUBSCRIPTION
            # =====================================

            open_access = "No"
            subscription = "No"

            if (
                "open access"
                in detail_text.lower()
                or
                "gold open access"
                in detail_text.lower()
            ):

                open_access = "Yes"

            if (
                "subscription"
                in detail_text.lower()
            ):

                subscription = "Yes"

            # =====================================
            # FINAL JSON
            # =====================================

            journal = {

                "title":
                    title,

                "link":
                    journal_url,

                "impact_factor":
                    impact_factor,

                "CiteScore":
                    citescore,

                "submission_to_first_decision":
                    first_decision,

                "Acceptance_to_publication":
                    acceptance_to_publication,

                "publication_charge":
                    publication_charge,

                "Open access":
                    open_access,

                "subscription":
                    subscription
            }

            all_journals.append(
                journal
            )

        except Exception as e:

            print(
                f"Error: {e}"
            )

    driver.quit()

    # =====================================
    # REMOVE DUPLICATES
    # =====================================

    unique_journals = []
    seen = set()

    for item in all_journals:

        if item["title"] not in seen:

            seen.add(
                item["title"]
            )

            unique_journals.append(
                item
            )

    return unique_journals