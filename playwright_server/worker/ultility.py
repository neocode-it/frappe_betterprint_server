import re
import html

def strip_tags(content : str) -> str:
    """Strip html tags from string"""
    return html.escape(content)

def strip_script_tags(content : str) -> str:
    return re.sub(r'<script[\s\S]*?>[\s\S]*?<\/script>', '', content, flags=re.DOTALL)