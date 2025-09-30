import asyncio
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai import CrawlerRunConfig,AsyncWebCrawler
async def filter():
    bm25_filter = BM25ContentFilter(
        user_query="BROCHURE on PAY & ALLOWANCES FOR THE YEAR",
        bm25_threshold=0.5,
        language="english"
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=bm25_filter,
        options={"ignore_links": True}
    )

    async with AsyncWebCrawler() as crawler:
        result=await crawler.arun("https://doe.gov.in/annual-report-pay-and-allowances",config=CrawlerRunConfig(markdown_generator=md_generator))
        if result.success:
            print(result.markdown.fit_markdown)
            with open(r"C://Users/Sai.jetti/Desktop/savings/BM25_markdowm.md","w",encoding="utf-8") as f:
                f.write(result.markdown.fit_markdown)

if __name__ == "__main__":
    asyncio.run(filter())



