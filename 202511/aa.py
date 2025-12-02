import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ---------- 1. Start Selenium browser and login ----------

def start_browser():
    options = Options()
    # add any options you normally use
    # options.add_argument("--headless")  # if you want headless
    browser = webdriver.Chrome(options=options)
    return browser

# ---------- 2. Build a requests.Session from the browser ----------

def make_metricstream_session(browser):
    session = requests.Session()

    # copy ALL cookies from browser into requests session
    for c in browser.get_cookies():
        name = c["name"]
        value = c["value"]
        domain = c.get("domain") or "bmo.a08a.metricstream.com"
        session.cookies.set(name, value, domain=domain)

    # headers – base them on your curl output
    ua = browser.execute_script("return navigator.userAgent;")

    headers = {
        "Accept": "application/octet-stream,application/json",
        "Accept-Language": "en-US,en;q=0.9,en-CA;q=0.8,fr-FR;q=0.7,fr;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://bmo.a08a.metricstream.com/",
        "User-Agent": ua,
    }

    # CSRF header must match XSRF-TOKEN cookie
    xsrf = session.cookies.get("XSRF-TOKEN")
    if xsrf:
        headers["X-Csrf-Token"] = xsrf

    session.headers.update(headers)
    return session

# ---------- 3. Download helper with simple retry ----------

def download_file(session, url, out_path, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        resp = session.get(url, stream=True)
        print(f"{url} -> {resp.status_code} (attempt {attempt})")

        if resp.status_code == 200:
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            return True

        if resp.status_code == 401 and attempt < max_attempts:
            # short backoff, but 401 here usually means tokens/cookies expired
            time.sleep(3)
            continue

        resp.raise_for_status()
    return False

# ---------- 4. Main ----------

def main():
    browser = start_browser()

    # go to login page and let YOU log in
    browser.get("https://bmo.a08a.metricstream.com/")  # adjust if needed
    input("Log in in the browser, then press Enter here to continue...")

    session = make_metricstream_session(browser)

    # list of download URLs (exactly like the curl URL)
    file_urls = [
        # example – replace with your own
        "https://bmo.a08a.metricstream.com/metricstream/api/7.0/documents/2014535566/binary?task_id=T-107273-20318047-0&fieldname=DO_DOCUMENT",
        # add more URLs here...
    ]

    for i, url in enumerate(file_urls, start=1):
        out_name = f"file_{i}.bin"  # or build from task_id / doc id
        ok = download_file(session, url, out_name)
        if not ok:
            print(f"FAILED: {url}")
        time.sleep(1)  # small delay between downloads

    browser.quit()

if __name__ == "__main__":
    main()