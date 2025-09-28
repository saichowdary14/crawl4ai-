from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
import asyncio

async def main():
    fit_md_generator = DefaultMarkdownGenerator(
        content_source="fit_html",
        options={"ignore_links": True}
    )

    config = CrawlerRunConfig(
        markdown_generator=fit_md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://nreganarep.nic.in/netnrega/app_issue.aspx?page=s&lflag=eng&state_name=ANDHRA%20PRADESH&state_code=02&fin_year=2025-2026&source=national&Digest=Rii51QmEgPjTfpD0tRPM2g", config=config)
        if result.success:
            print("Markdown fetched successfully.")
            html_content = result.cleaned_html            

            file_path = r"C:\Users\hp\Desktop\savings\full_html.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print("html  saved to full_htnl.html")
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
