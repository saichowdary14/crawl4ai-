from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler,LLMConfig
import json
from typing import List
import asyncio
import pandas as pd
from pathlib import Path
import os
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai import CrawlerRunConfig

async def bm25filter():
    bm25_filter = BM25ContentFilter(
    user_query="machine learning",
    bm25_threshold=1.2,
    language="english"
        )

    md_generator = DefaultMarkdownGenerator(
    content_filter=bm25_filter,
    options={"ignore_links": True}
)

    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com/docs", config=config)
        if result.success:
            print("rawMarkdown:\n", result.markdown[:500])  # Just a snippet
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    import asyncio
    # asyncio.run(main())


#_________________________________________________________________________
#_________________________________________________________________________

async def fit_markdown():
    # Example: ignore all links, don't escape HTML, and wrap text at 80 characters
    raw_md_generator = DefaultMarkdownGenerator(
        content_source="fit_html",
        options={"ignore_links": True}
    )

    config = CrawlerRunConfig(
        markdown_generator=raw_md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com/docs", config=config)
        if result.success:
            print("fitMarkdown:\n", result.markdown[:500])  # Just a snippet
            
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(fit_markdown())