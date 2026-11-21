import os
import re

import allure
from typing import Iterator
from playwright.sync_api import Playwright, Page
from config import settings, Browser


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: Browser,
        storage_state: str | None = None
) -> Iterator[Page]:

    os.makedirs("./tracing", exist_ok=True)
    os.makedirs("./videos", exist_ok=True)

    browser = playwright[browser_type].launch(headless=settings.headless)
    context = browser.new_context(storage_state=storage_state, record_video_dir=settings.videos_dir)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    safe_test_name = re.sub(r'[\\/*?:"<>|]', "_", test_name)
    trace_path = settings.tracing_dir.joinpath(f"{safe_test_name}.zip")
    context.tracing.stop(path=trace_path)

    video_path = page.video.path()

    browser.close()

    if os.path.exists(trace_path):
        allure.attach.file(
            source=trace_path,
            name="trace",
            attachment_type=allure.attachment_type.ZIP
        )
    else:
        print(f"Не удалось найти файл трейса для аттача: {trace_path}")

    if video_path and os.path.exists(video_path):
        allure.attach.file(
            source=video_path,
            name="video",
            attachment_type=allure.attachment_type.WEBM
        )
    else:
        print(f"Не удалось найти файл видео для аттача: {video_path}")
