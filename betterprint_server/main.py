import sys

from betterprint_server.server.start_server import start_server

def main():
    if "--help" in sys.argv[1:]:
        print("Playwright Server for playwright-print Frappe app. Usage `betterprint_server run`")
        exit(0)
    elif "run" in sys.argv[1:]:
        start_server()
    elif "run-public" in sys.argv[1:]:
        start_server(True)

if __name__ == "__main__":
    main()