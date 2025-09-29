import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig,DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.deep_crawling import DFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
import json
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

async def solve_captcha_text(captcha_html_file_path):

    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o",
            api_token=os.getenv('OPENAI_API_KEY')
        ),
        instruction="This HTML contains a captcha challenge. Solve it and return ONLY the numeric answer."
    )

    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
    captcha_file_url = f"file://{Path(captcha_html_file_path).resolve()}"
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=captcha_file_url, config=config)
        if result.success:
            data = json.loads(result.extracted_content)
            for item in data:
                captcha_content = item.get("content", [])
                if captcha_content:
                    captcha_value = captcha_content[0]
                    print("Captcha:", captcha_value)
                    return captcha_value
                break  # if only one item is neede

  #______________________________________________________________________________________________
  # ______________________________________________________________________________________________  



async def extract_subheadings_with_crawl4ai( user_prompt : str,full_html_file_path ):

    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o",
            api_token=os.getenv('OPENAI_API_KEY')
        ),
        instruction = (
    f"You are given the full HTML of a page. On this page, there are multiple main headings. "
    f"Each main heading contains one or more subheadings, and each subheading is a link. "
    f"Your task is to find the subheading that matches the user's input: '{user_prompt}' "
    f"and return its associated link."

    f"\n\nReturn a JSON array with the following format:"
    f"\n[\n  {{"
    f'\n    "index": <int>,'
    f'\n    "tags": ["<tag>"],'
    f'\n    "content": ["<subheading_text>", "<link_url>"],'
    f'\n    "error": false'
    f"\n  }}\n]"

    f"\n\nOnly include the subheading that matches or closely matches '{user_prompt}'."
    f"\nBe precise and do not invent subheadings or links."
))

    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
    full_html_file_url = f"file://{Path(full_html_file_path).resolve()}"
    

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=full_html_file_url, config=config)
        if result.success:
            try:
                data = json.loads(result.extracted_content)
                for item in data:
                    total_content= item.get("content", [])
                    print(total_content)
                    if total_content[0].lower() in user_prompt.lower():
                        print(f"you want the data from {total_content[0]}")
                        return total_content[1]
                    break
    
            except Exception as e:
                print("❌ Error parsing extracted content:", e)

        else:
            print("not found data")
#______________________________________________________________________________________________
#_____________________________________________________________________________________________


async def cleaned_html(url):
    fit_md_generator = DefaultMarkdownGenerator(
        content_source="fit_html",
        options={"ignore_links": True}
    )

    config = CrawlerRunConfig(
        markdown_generator=fit_md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url,config=config)
        if result.success:
            print("html fetched successfully.")
            html_content = result.cleaned_html
            return html_content
        else:
            print("no data found")       

#________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________
async def table_extraction(html_file_path):
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o",
            api_token=os.getenv('OPENAI_API_KEY')
        ),
    extraction_type="block",  # Extract free-form content blocks
    instruction="""
From the html page  i want only all the tr tags data in seperate lists from the main table i want header row also
if multi header row make sure to make it one row based on the data row of the table
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
        # html_file_path = r"C:\Users\hp\Desktop\savings\full_html.html"
        file_url = f"file://{Path(html_file_path).resolve()}"
        results:type[List]= await crawler.arun(url=file_url, config=config)

        print("fetching the table data")
        if results.success:
            data = json.loads(results.extracted_content)
            return data
        else:
            print("no data found")