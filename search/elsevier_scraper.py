# =====================================
# elsevier_scraper.py
# =====================================

from scrapling.fetchers import StealthyFetcher
from urllib.parse import quote_plus
import re
import time

BASE_URL = (
    "https://journalfinder.elsevier.com/results"
)

# =====================================
# SEARCH ELSEVIER
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

    print(f"\n[*] Searching Elsevier...")
    print(f"[*] URL: {url}")

    # =====================================
    # FETCH SEARCH PAGE
    # =====================================

    page = StealthyFetcher.fetch(
        url,
        headless=True,
        network_idle=True,
    )

    print(f"[*] Status: {page.status}")

    # =====================================
    # RESULT CARDS
    # =====================================

    cards = page.css("article")

    if not cards:
        cards = page.css("div")

    print(f"[*] Found {len(cards)} results")

    # =====================================
    # LOOP RESULTS
    # =====================================

    for idx, card in enumerate(
        cards,
        start=1
    ):

        try:

            print(f"\n======================")
            print(f"Processing Result {idx}")
            print(f"======================")

            detail_text = card.text

            # DEBUG
            print(detail_text)

            # =====================================
            # TITLE
            # =====================================

            title = "N/A"

            title_el = card.css("h2")

            if title_el:

                title = (
                    title_el[0]
                    .text
                    .strip()
                )

            # =====================================
            # URL
            # =====================================

            links = card.css("a")

            journal_url = None

            for a in links:

                href = a.attrib.get(
                    "href",
                    ""
                )

                if not href:
                    continue

                if href.startswith("/"):

                    href = (
                        "https://journalfinder.elsevier.com"
                        + href
                    )

                if (
                    "journal" in href.lower()
                    or "sciencedirect" in href.lower()
                    or "elsevier" in href.lower()
                ):

                    journal_url = href

                    break

            if not journal_url:

                print(
                    "[!] No journal URL found"
                )

                continue

            # =====================================
            # IMPACT FACTOR
            # =====================================

            impact_factor = None

            if (
                "Impact Factor"
                in detail_text
            ):

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

            citescore = None

            if (
                "CiteScore"
                in detail_text
            ):

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
            # FIRST DECISION
            # =====================================

            first_decision = None

            if (
                "Submission to first decision"
                in detail_text
            ):

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
            # PUBLISHING MODEL
            # =====================================

            publishing_model = (
                "Subscription"
            )

            if (
                "Open Access"
                in detail_text
                or
                "Gold Open Access"
                in detail_text
            ):

                publishing_model = (
                    "Open Access"
                )

            # =====================================
            # SAVE
            # =====================================

            journal = {

                "journal_name":
                    title,

                "impact_factor":
                    impact_factor,

                "citescore":
                    citescore,

                "submission_to_first_decision":
                    first_decision,

                "publishing_model":
                    publishing_model,

                "publisher":
                    "Elsevier",

                "url":
                    journal_url
            }

            yield journal

            print(
                f"[OK] Added: {title}"
            )

            time.sleep(0.1)

        except Exception as e:

            print(
                f"[!] Search Error: {e}"
            )