from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import asyncio
import json
import pandas as pd

async def main():
    # Extraction strategy (supports schema)
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(),
        instruction="""
        From the given webpage, extract the table related to Annual Report on Pay and Allowances.
        Extract only the table data with keys: Title, Year, Download_link
        """,
        schema='{"Title":"string","Year":"string","Download_link":"string"}',
        verbose=True
    )

    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://doe.gov.in/annual-report-pay-and-allowances", config=config)

        if result.success:
            print(result.extracted_content)  # JSON string

            # Save JSON
            with open(r"C://Users/Sai.jetti/Desktop/savings/LLM_table.json", "w", encoding="utf-8") as f:
                f.write(result.extracted_content)

            # Save Excel
            data = json.loads(result.extracted_content)
            df = pd.DataFrame(data)
            df.to_excel(r"C://Users/Sai.jetti/Desktop/savings/LLM_table.xlsx", index=False)
        else:
            print("Data not found")

if __name__ == "__main__":
    asyncio.run(main())
