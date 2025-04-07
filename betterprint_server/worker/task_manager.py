from betterprint_server.worker.ultility import (
    strip_tags,
    playwright_add_cors_allow_route,
)
from urllib.parse import urlparse


def manage_task(task, browser):
    if task["command"] == "calculate-element-heights":
        return calculate_element_heights(task, browser)

    elif task["command"] == "generate-pdf":
        return generate_pdf(task, browser)

    elif task["command"] == "generate-betterprint-pdf":
        return generate_betterprint_pdf(task, browser)

    elif task["command"] == "split-table-by-height":
        return split_table_by_height(task, browser)

    else:
        return {"error": True, "description": "WORKER ERROR: Command not found"}


def calculate_element_heights(task, browser) -> dict:
    page = browser.new_page()
    page.set_content(task["html"])
    from betterprint_server.worker.js import get_element_height

    heights = page.evaluate(get_element_height, strip_tags(task["element"]))
    page.close()
    return {"content": heights}


def split_table_by_height(task, browser) -> dict:
    page = browser.new_page()
    page.set_content(task["html"])

    from betterprint_server.worker.js import split_table_by_maxheight

    pages = page.evaluate(split_table_by_maxheight, task["max-height"])

    page.close()
    return {"content": pages}


def generate_pdf(task, browser):
    page = browser.new_page()
    page_width = f"{task.get('page-width', 210)}mm"
    page_height = f"{task.get('page-height', 297)}mm"

    page.set_content(task["html"])

    page.pdf(width=page_width, height=page_height, path=task["filepath"])

    page.close()
    return {"content": "successful"}


def generate_betterprint_pdf(task: dict, browser) -> dict:
    """
    Generates a PDF from HTML content, waiting for a custom event or timeout.
    """

    # TODO: Implement page size (Maybe first complete frappes-app implementation?)
    # TODO: Implement CORS with proper regex
    # TODO: Implement Browser/Pagedjs error handling and return in case of exceptions

    page = browser.new_page()

    # # Convert origin url into origin domain
    # parsed_url = urlparse(task["allow_origin"])
    # full_domain = parsed_url.netloc
    # domain = full_domain.split(":")[0]  # Remove the port if present

    # # Ignore CORS for this domain
    # # Workaround for: Chrome will always block CORS for local html files
    # playwright_add_cors_allow_route(page, domain)

    # Add page content
    page.set_content(task["html"])

    try:
        # Wait for the "betterPrintFinished" event with a timeout of 30 seconds (30000 ms)
        page.evaluate("""
            document.addEventListener('betterPrintFinished', () => {
                window.betterPrintFinished = true;
            });
        """)

        page.wait_for_function("window.betterPrintFinished === true", timeout=30000)

        dimensions = page.evaluate("""() => {
            const page = document.querySelector(".paginatejs-pages .page");
            const style = getComputedStyle(page);
            const width = style.width;
            const height = style.height;
            return {"width": width, "height": height};
            }
        """)
    except Exception:
        return {
            "content": "failed",
            "error": "Unknown failure printing PDF",
        }

    # page.pdf(width=page_width, height=page_height, path=task["filepath"])
    page.pdf(
        width=dimensions["width"], height=dimensions["height"], path=task["filepath"]
    )

    return {"content": "successful"}
