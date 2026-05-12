"""
Springer Journal Finder
FINAL VERSION

Features:
- Abstract -> Keyword Extraction
- Springer Search
- Extract Journal Metrics
- Save ALL Results in JSON
"""

from scrapling.fetchers import StealthyFetcher
from urllib.parse import quote_plus
import json
import re
import time


BASE_URL = "https://link.springer.com/search"
OUTPUT_FILE = "journal.json"


# =====================================
# Keyword Extraction
# =====================================

def extract_keywords(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    stopwords = {
        "the", "is", "a", "an", "and", "or",
        "for", "to", "of", "in", "on", "with",
        "this", "that", "we", "will", "are",
        "be", "from", "by", "as", "at"
    }

    words = []

    for word in text.split():

        if word not in stopwords and len(word) > 2:
            words.append(word)

    return " ".join(words[:10])


# =====================================
# Extract Journal Metrics
# =====================================

def extract_journal_metrics(journal_url):

    metrics = {

        "journal_name": "N/A",
        "impact_factor": "N/A",
        "submission_to_first_decision": "N/A",
        "publishing_model": "N/A"
    }

    try:

        print(f"\n   [->] Opening Journal: {journal_url}")

        page = StealthyFetcher.fetch(
            journal_url,
            headless=True,
            network_idle=True,
        )

        html = page.html_content

        # =========================
        # Journal Name
        # =========================

        name_match = re.search(
            r'<h1[^>]*>(.*?)</h1>',
            html,
            re.DOTALL | re.IGNORECASE
        )

        if name_match:

            name = re.sub(
                r"<.*?>",
                "",
                name_match.group(1)
            )

            metrics["journal_name"] = name.strip()

        # =========================
        # Impact Factor
        # =========================

        impact_match = re.search(
            r'Impact factor[^0-9]*([\d.]+)',
            html,
            re.IGNORECASE
        )

        if impact_match:

            metrics["impact_factor"] = (
                impact_match.group(1)
            )

        # =========================
        # Submission to First Decision
        # =========================

        decision_match = re.search(
            r'Submission to first decision[^0-9]*(\d+\s*days)',
            html,
            re.IGNORECASE
        )

        if decision_match:

            metrics["submission_to_first_decision"] = (
                decision_match.group(1)
            )

        # =========================
        # Publishing Model
        # =========================

        if "Hybrid" in html:

            metrics["publishing_model"] = "Hybrid"

        elif "Open access" in html:

            metrics["publishing_model"] = "Open Access"

    except Exception as e:

        print(f"[!] Metrics Error: {e}")

    return metrics


# =====================================
# Search Springer
# =====================================

# def search_springer(query):

#     encoded_query = quote_plus(query)

#     url = (
#         f"{BASE_URL}"
#         f"?query={encoded_query}"
#         f"&search-within=Journals"
#     )

#     print(f"\n[*] Searching Springer...")
#     print(f"[*] URL: {url}")

#     page = StealthyFetcher.fetch(
#         url,
#         headless=True,
#         network_idle=True,
#     )

#     print(f"[*] Status: {page.status}")

#     cards = page.css("li.app-card-open")

#     if not cards:
#         cards = page.css("article")

#     print(f"[*] Found {len(cards)} results")

#     journals = []

#     visited = set()

#     # =====================================
#     # LOOP THROUGH ALL RESULTS
#     # =====================================

#     for idx, card in enumerate(cards, start=1):

#         try:

#             print(f"\n======================")
#             print(f"Processing Result {idx}")
#             print(f"======================")

#             links = card.css("a")

#             journal_url = None

#             for a in links:

#                 href = a.attrib.get("href", "")

#                 if "/journal/" in href:

#                     if href.startswith("/"):

#                         journal_url = (
#                             "https://link.springer.com" + href
#                         )

#                     else:
#                         journal_url = href

#                     break

#             if not journal_url:

#                 print("[!] No journal URL found")
#                 continue

#             # avoid duplicate journals
#             if journal_url in visited:

#                 print("[!] Duplicate skipped")
#                 continue

#             visited.add(journal_url)

#             # =========================
#             # Extract Metrics
#             # =========================

#             metrics = extract_journal_metrics(
#                 journal_url
#             )

#             metrics["url"] = journal_url

#             metrics["publisher"] = "Springer"

#             journals.append(metrics)

#             print(
#                 f"[OK] Added: "
#                 f"{metrics['journal_name']}"
#             )

#             # avoid blocking
#             time.sleep(1)

#         except Exception as e:

#             print(f"[!] Search Error: {e}")

#     return journals


# =====================================
# Search Springer
# =====================================

def search_springer(query):

    encoded_query = quote_plus(query)

    url = (
        f"{BASE_URL}"
        f"?query={encoded_query}"
        f"&search-within=Journals"
    )

    print(f"\n[*] Searching Springer...")
    print(f"[*] URL: {url}")

    page = StealthyFetcher.fetch(
        url,
        headless=True,
        network_idle=True,
    )

    print(f"[*] Status: {page.status}")

    cards = page.css("li.app-card-open")

    if not cards:
        cards = page.css("article")

    print(f"[*] Found {len(cards)} results")

    journals = []

    # =====================================
    # LOOP THROUGH ALL RESULTS
    # =====================================

    for idx, card in enumerate(cards, start=1):

        try:

            print(f"\n======================")
            print(f"Processing Result {idx}")
            print(f"======================")

            links = card.css("a")

            journal_url = None

            for a in links:

                href = a.attrib.get("href", "")

                if "/journal/" in href:

                    if href.startswith("/"):

                        journal_url = (
                            "https://link.springer.com" + href
                        )

                    else:
                        journal_url = href

                    break

            if not journal_url:

                print("[!] No journal URL found")
                continue

            # =========================
            # Extract Metrics
            # =========================

            metrics = extract_journal_metrics(
                journal_url
            )

            metrics["url"] = journal_url

            metrics["publisher"] = "Springer"

            journals.append(metrics)

            print(
                f"[OK] Added: "
                f"{metrics['journal_name']}"
            )

            # avoid blocking
            time.sleep(0.2)

        except Exception as e:

            print(f"[!] Search Error: {e}")

    return journals


# =====================================
# Save JSON
# =====================================

def save_results(results):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\n[OK] Saved "
        f"{len(results)} journals "
        f"to {OUTPUT_FILE}"
    )


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    abstract = input("\nEnter Abstract:\n\n")

    # =====================================
    # Extract Keywords
    # =====================================

    keywords = extract_keywords(abstract)

    print(f"\n[*] Extracted Keywords:")
    print(keywords)

    # =====================================
    # Search Journals
    # =====================================

    results = search_springer(keywords)

    # =====================================
    # Save JSON
    # =====================================

    save_results(results)

    # =====================================
    # Console Output
    # =====================================

    print("\n========== FINAL RESULTS ==========\n")

    for j in results:

        print(f"Journal: {j['journal_name']}")

        print(
            f"Impact Factor: "
            f"{j['impact_factor']}"
        )

        print(
            f"First Decision: "
            f"{j['submission_to_first_decision']}"
        )

        print(
            f"Publishing Model: "
            f"{j['publishing_model']}"
        )

        print(f"URL: {j['url']}")

        print("-" * 60)

