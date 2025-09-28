from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler,LLMConfig
import json
from typing import List
import asyncio
import pandas as pd
from pathlib import Path
import os

async def table_extraction(local_file_path):
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o",
            api_token=os.env('gpt')
        ),
    extraction_type="block",  # Extract free-form content blocks
    instruction="""
From the html page  i want only all the tr tags data in seperate lists from the main table
    """,
    apply_chunking=True,
    chunk_token_threshold=1200,
    input_format="fit_markdown"  # Use cleaned content
)

    config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        verbose=True,
        exclude_external_links=True,
        excluded_tags=['nav', 'footer', 'aside', 'advertisement']
    )

    async with AsyncWebCrawler() as crawler:
        local_md_path = r"C:\Users\hp\Desktop\savings\full_html.html"
        file_url = f"file://{Path(local_file_path).resolve()}"
        results:type[List]= await crawler.arun(url=file_url, config=config)

        if results.success:
            # print(results.extracted_content)
            data = json.loads(results.extracted_content)
            return data
            lists=[]
            for item in data:
                flat_data = item["content"]
                lists.append(flat_data)
            df=pd.DataFrame(lists)
            print(df)
            save_path=r"C:\Users\hp\Desktop\savings\table.csv"
            df.to_csv(save_path,index=False)
            


if __name__ == "__main__":
    local_md_path = r"C:\Users\hp\Desktop\savings\full_html.html"  # Path to your markdown file
    asyncio.run(table_extraction(local_md_path))
