import sys

from playwright_server.server.start_server import start_server

def main():
    if "--help" in sys.argv[1:]:
        print("Playwright Server for playwright-print Frappe app. Usage `playwright_server run`")
        exit(0)
    elif "run" in sys.argv[1:]:
        start_server()

if __name__ == "__main__":
    main()