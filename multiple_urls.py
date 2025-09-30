from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler,LLMConfig
import json
from typing import List
import asyncio
import pandas as pd
from pathlib import Path
import os

import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_multiple(urls):
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls)
        for result in results:
            print("URL:", result.url)
            print("Clean Markdown:", result.markdown)
            print("----")

if __name__ == "__main__":
    urls = ["https://www.example.com", "https://www.wikipedia.org"]
    asyncio.run(crawl_multiple(urls))

