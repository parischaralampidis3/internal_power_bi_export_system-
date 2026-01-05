from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def export_png_from_iframe(iframe_url: str, output_path:str, wait_seconds: int = 5):

    output_path = Path(output_path)
    output_path.parent.mkdir(parents= True, exist_ok = True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport = {"width": 1920, "height": 1080}
        )

        page = context.new_page()

        page.goto(iframe_url, timeout=60_000)

        page.wait_for_load_state("networkidle")

        page.wait_for_timeout(5000)  # wait for 5 seconds to ensure content is loaded

        page.pdf(
            path=output_path,
            format = "A4",
            print_background=True
        )
        browser.close()
    
    return str(output_path)