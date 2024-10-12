from betterprint_server.worker.ultility import strip_tags

def manage_task(task, browser):
    if task['command'] == 'calculate-element-heights':
        return calculate_element_heights(task, browser)
    
    elif task['command'] == 'generate-pdf':
        return generate_pdf(task, browser)
    
    elif task['command'] == 'split-table-by-height':
        return split_table_by_height(task, browser)
    
    else:
        return {
            "error": True,
            "description": "WORKER ERROR: Command not found"
        }

def calculate_element_heights(task, browser) -> dict:
    html = html_wrapper(task['html'], strip_tags(task['style']))
    page = browser.new_page()
    page.set_content(html)
    heights = page.evaluate('''
        (selector) => {
        const elements = document.querySelectorAll(selector);
        const heights = [];
        elements.forEach(element => {
            heights.push(Math.round(element.offsetHeight * 0.26458));
        });
        return heights;
    }''', strip_tags(task['element']))
    page.close()
    return {'content': heights}

def split_table_by_height(task, browser) -> dict:
    page = browser.new_page()
    page.set_content(task['html'])


    from betterprint_server.worker.js import split_table_by_maxheight
    pages = page.evaluate(split_table_by_maxheight, task['max-height'])
    
    page.close()
    return {'content': pages}

def generate_pdf(task, browser):
    page = browser.new_page()
    page.set_content(task['html'])
    page.pdf(path=task['filepath'])
    page.close()
    return {'content': 'successful'}
