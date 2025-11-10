from selenium import webdriver
import requests

driver = webdriver.Chrome()
driver.get("https://example.com/login")
# ... do login, navigate to listing ...

all_links = []

while True:
    # find all download anchors
    links = [a.get_attribute("href") for a in driver.find_elements("css selector", "a.download-link")]
    all_links.extend(links)

    # check if there is a "next page"
    next_btns = driver.find_elements("css selector", "a.next-page")
    if not next_btns:
        break
    next_btns[0].click()

# move cookies from selenium to requests
s = requests.Session()
for c in driver.get_cookies():
    s.cookies.set(c["name"], c["value"], domain=c.get("domain"))

driver.quit()

# now download with requests, not Selenium
import os

os.makedirs("downloads", exist_ok=True)

for i, url in enumerate(all_links, 1):
    filename = os.path.join("downloads", f"file_{i}.zip")
    with s.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)