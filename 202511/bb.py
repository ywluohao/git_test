import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options


BASE_URL = "https://bmo.a08a.metricstream.com/"


def build_requests_session_from_driver(driver) -> requests.Session:
    """Copy cookies + user agent from Selenium driver into a requests.Session."""
    session = requests.Session()

    # 1) Copy all cookies
    for c in driver.get_cookies():
        session.cookies.set(c["name"], c["value"])

    # 2) User-Agent from the real browser
    ua = driver.execute_script("return navigator.userAgent;")
    session.headers.update({
        "User-Agent": ua,
        "Accept": "application/octet-stream,application/json",
        "Referer": BASE_URL,
        "Connection": "keep-alive",
    })

    # 3) If you have tokens in localStorage / sessionStorage, grab them here
    #    (example; adjust the key name to your real one)
    try:
        x_card_token = driver.execute_script(
            "return window.localStorage.getItem('x-card-token');"
        )
        if x_card_token:
            session.headers["x-card-token"] = x_card_token
    except Exception:
        pass

    return session


def guess_filename(url: str) -> str:
    return urlparse(url).path.split("/")[-1] or "download.bin"


def download_with_session(session: requests.Session, url: str, out_path: str | None = None) -> str:
    if out_path is None:
        out_path = guess_filename(url)

    resp = session.get(url, stream=True)
    if resp.status_code == 401:
        raise RuntimeError("401 Unauthorized – your cookies/tokens from Selenium are not valid.")
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)

    return out_path


if __name__ == "__main__":
    # ==== 1. Start Selenium and log in ====
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    service = EdgeService()  # or EdgeService("msedgedriver.exe") if needed
    driver = webdriver.Edge(service=service, options=edge_options)

    driver.get(BASE_URL)
    # TODO: put your login / navigation steps here (clicks, send_keys, etc.)
    # Make sure you are fully logged in and can open a document manually.
    time.sleep(20)  # replace with explicit waits in your real script

    # ==== 2. Build requests session from Selenium ====
    session = build_requests_session_from_driver(driver)

    # ==== 3. Use that session to download by URL ====
    # input URL – this is the same URL you pass to curl, e.g.:
    # https://bmo.a08a.metricstream.com/metricstream/api/7.0/documents/2014535566/binary?task_id=...
    url_to_download = input("Paste document URL: ").strip()
    out_file = download_with_session(session, url_to_download)
    print(f"Saved to {out_file}")

    driver.quit()