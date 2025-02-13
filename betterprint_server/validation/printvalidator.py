import os


def is_valid_pdf_filepath(filepath: str) -> bool:
    """Validate if the given path is a valid pdf filepath.
    Doesn't check if the path exists"""
    try:
        if not os.path.isabs(filepath) or os.path.isdir(filepath):
            return False

        if not filepath.endswith(".pdf"):
            return False

        return False
    except Exception as e:
        return False
