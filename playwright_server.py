from playwright.sync_api import sync_playwright
import os



def main():
    print("Hello from playwright-server!")


if __name__ == "__main__":
    main()


def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://playwright.dev")
        page.screenshot(path="example.png")
        print(page.title())
        browser.close()

    print('Finished :)')
    print(os.path.abspath(__file__))