import re
import html

from playwright.sync_api import sync_playwright

def manage_task(task, browser):
    if task['command'] == 'calculate-element-heights':
        return calculate_element_heights(task, browser)
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
