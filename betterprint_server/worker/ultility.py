import re


def strip_tags(content: str) -> str:
    """Strip html tags from string"""
    return re.sub(
        r"<[^>]*>|<|>", "", content
    )  # Strip any tags or even single angle brackets


def strip_script_tags(content: str) -> str:
    return re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>", "", content, flags=re.DOTALL)


def html_wrapper(body: str, style: str) -> str:
    return f"""
    <!DOCTYPE html>
        <head>
            <meta charset="UTF-8">
            <title>PRINT</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <style>{style}</style>
        </head>
        <body>
            {body}
        </body>
    </html> 
    """


def modify_playwright_cors(route, allow_domain):
    try:
        domain_pattern = rf"^https?://{re.escape(allow_domain)}(:[0-9]+)?(/|$)"

        if re.match(domain_pattern, route.request.url):
            response = route.fetch()
            headers = response.headers.copy()
            headers["Access-Control-Allow-Origin"] = "*"
            route.fulfill(status=response.status, headers=headers, body=response.body())
        else:
            route.continue_()
    except Exception as e:
        route.continue_()
