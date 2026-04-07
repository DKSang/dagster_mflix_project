import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
TARGET_URL = os.environ.get(
    "PTIT_TARGET_URL",
    "https://code.ptit.edu.vn/student/contest/K051UW1jVXdxZEl3WEFBc2M1OWNBZz09",
)
LOGIN_URL = "https://code.ptit.edu.vn/login"
OUTPUT_HTML_PATH = Path(os.environ.get("PTIT_OUTPUT_HTML", str(BASE_DIR / "output.html")))


def login_and_fetch_html(target_url: str) -> str:
    username = os.environ.get("PTIT_USERNAME")
    password = os.environ.get("PTIT_PASSWORD")
    if not username or not password:
        raise SystemExit("Missing PTIT_USERNAME or PTIT_PASSWORD environment variables.")

    session = requests.Session()
    response = session.get(target_url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    form = soup.find("form")
    if form is None:
        return response.text

    token_input = form.find("input", attrs={"name": "_token"})
    login_payload = {
        "_token": token_input.get("value", "") if token_input else "",
        "username": username,
        "password": password,
        "remember": "1",
    }

    login_action = form.get("action") or LOGIN_URL
    login_response = session.post(
        login_action,
        data=login_payload,
        timeout=30,
        headers={"Referer": response.url},
    )
    login_response.raise_for_status()

    final_response = session.get(target_url, timeout=30)
    final_response.raise_for_status()
    if "/login" in final_response.url:
        raise SystemExit("Login failed; the site still redirected to the login page.")
    return final_response.text


html = login_and_fetch_html(TARGET_URL)
soup = BeautifulSoup(html, "html.parser")

with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as file_handle:
    file_handle.write(soup.prettify())