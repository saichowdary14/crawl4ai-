from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMConfig, DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import LLMContentFilter
import asyncio
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    url="https://nreganarep.nic.in/netnrega/MISreport4.aspx"
    page.goto(url)

async def capcha():
    # Initialize LLM filter with specific instruction
    filter = LLMContentFilter(
        llm_config = LLMConfig(), #or use environment variable
        instruction="""
        from the given webpage. there is a captha so solve it and get the solution .then fill that solution inthat respective box and press verify code button
        """,
        chunk_token_threshold=1000,  # Adjust based on your needs
        verbose=True
    )
    md_generator = DefaultMarkdownGenerator(
        content_filter=filter,
        options={"ignore_links": True}
    )
    config = CrawlerRunConfig(
        markdown_generator=md_generator,
    )
    browser_cfg = BrowserConfig(headless=True, user_agent="MyCrawler/1.0")

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        if result.success:
            sol=(result.extracted_content)  # Filtered markdown content
            # with open(r"C://Users/Sai.jetti/Desktop/savings/llm_capcha.md","w",encoding="utf-8") as f:
            #     f.write(result.markdown.fit_markdown)
        else:
            print("not found data")

if __name__=="__main__":
    asyncio.run(capcha())


