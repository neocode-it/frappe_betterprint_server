from playwright.sync_api import sync_playwright



def main():
    print("Hello from playwright-server!")


if __name__ == "__main__":
    main()


def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://playwright.dev")
        print(page.title())
        browser.close()

    print('Finished :)')