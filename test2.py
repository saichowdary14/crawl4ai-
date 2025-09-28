import asyncio
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler
from crawl4ai.deep_crawling import DFSDeepCrawlStrategy
from bs4 import BeautifulSoup

async def run_deep_crawl(url):
    # Configure the crawler for DFS deep crawl with max depth 2
    config = CrawlerRunConfig(
        deep_crawl_strategy=DFSDeepCrawlStrategy(max_depth=2,include_external=False),
        verbose=True,
        page_timeout=150000,  # increase timeout to 120 seconds
        delay_before_return_html=1.0,  # small delay after load
        wait_until="domcontentloaded"   # prints crawling progress
        )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(url=url, config=config)


        for i,result in enumerate(results):
            print(f"first {i} {result}")
            if result.success:
                html=result.html
                print(html)
            #     break
            #     soup = BeautifulSoup(html, 'html.parser')
            #     th_elements = soup.find_all('th')
            #     if not th_elements:
            #         print(f"⚠️ No <th> elements found in page {i}.")
            #     else:
            #         header_texts = [th.get_text(strip=True) for th in th_elements]
            #         print(f"✅ <th> elements from page {i}:")
            #         print(header_texts)
            # else:
            #     print(f"❌ Failed to crawl page {i}.")
            #     break


    # Run the async crawl on a seed URL
asyncio.run(run_deep_crawl("https://nreganarep.nic.in/netnrega/app_issue.aspx?page=s&lflag=eng&state_name=ANDHRA%20PRADESH&state_code=02&fin_year=2025-2026&source=national&Digest=Rii51QmEgPjTfpD0tRPM2g"))