import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from utils import  extract_year_and_state_from_prompt
from lllm1 import solve_captcha_text,extract_subheadings_with_crawl4ai,cleaned_html,table_extraction
from urllib.parse import urljoin
import pandas as pd



#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------



# ✅ 3. Main Playwright automation flow
async def main():
    
    user_prompt = "I want the Ombudsperson Details for the year 2025-2026 of Nagaland"
    base_url = "https://nreganarep.nic.in/netnrega/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://nrega.dord.gov.in/MGNREGA_new/Nrega_home.aspx")

        # Close popup
        await page.locator('//*[@id="modalprogramme"]/div/div/div[1]/button').click()
        print("✅ Popup closed")

        # Open Annual Reports (new tab)
        async with context.expect_page() as new_page_event:
            await page.locator(
                '//*[@id="form1"]/div[3]/section[2]/div[3]/div/div/div[1]/div/p[2]/button'
            ).click()
        new_page = await new_page_event.value
        print("✅ Switched to new tab:", new_page.url)

        # Solve captcha
        await new_page.wait_for_load_state("networkidle")
        captcha_selector = "#ContentPlaceHolder1_lblStopSpam"
        await new_page.locator(captcha_selector).wait_for(state="visible", timeout=15000)

        captcha_text = await new_page.locator(captcha_selector).inner_text()
        print("🔑 Captcha text:", captcha_text)
        output_dir = Path("savings")  # relative to script
        output_dir.mkdir(exist_ok=True)  # create 'savings' folder if it doesn't exist
        captcha_html_file_path = output_dir / "captcha_html.html"
        with open(captcha_html_file_path, "w", encoding="utf-8") as f:
            f.write(f"<html><body><p>{captcha_text}</p></body></html>")

        solution = await solve_captcha_text(captcha_html_file_path)
        print("✅ Captcha solution:", solution)

        captcha_input = new_page.locator("#ContentPlaceHolder1_txtCaptcha")
        button = new_page.locator("#ContentPlaceHolder1_btnLogin")

        await captcha_input.wait_for(state="visible", timeout=20000)
        await button.wait_for(state="visible", timeout=20000)
        await captcha_input.fill(solution)
        await button.click()
        await asyncio.sleep(3)

        # Wait for dropdowns
        await new_page.locator('#ContentPlaceHolder1_ddlfinyr').wait_for(state='visible', timeout=10000)
        await new_page.locator('#ContentPlaceHolder1_ddl_States').wait_for(state='visible', timeout=10000)

        # ✅ Scrape dropdown options
        year_options = await new_page.locator('#ContentPlaceHolder1_ddlfinyr option').all_inner_texts()
        state_options = await new_page.locator('#ContentPlaceHolder1_ddl_States option').all_inner_texts()
        print("🔄 Year options:", year_options)
        print("🔄 State options:", state_options)

        # ✅ Match prompt → dropdown values
        matched_year, matched_state = extract_year_and_state_from_prompt(user_prompt, year_options, state_options)
        print(f"🎯 Matched Year: {matched_year}, Matched State: {matched_state}")

        # ✅ Select matched values
        if matched_year:
            await new_page.select_option('#ContentPlaceHolder1_ddlfinyr', label=matched_year)
            print(f"✅ Selected Year: {matched_year}")
        else:
            print("❌ Could not match year from prompt!")

        if matched_state:
            await new_page.select_option('#ContentPlaceHolder1_ddl_States', label=matched_state)
            print(f"✅ Selected State: {matched_state}")
        else:
            print("❌ Could not match state from prompt!")

        await asyncio.sleep(2)

        #-----------------------------------------------------------------
        #------------------------------------------------------------------

        full_page_html=await new_page.content()
        full_html_file_path = output_dir / "full_html.html"
        with open(full_html_file_path, "w", encoding="utf-8") as f:
            f.write(full_page_html)
        selected_link = await extract_subheadings_with_crawl4ai(user_prompt,full_html_file_path)
        print("✅ selected_link:", selected_link)
        final_link=urljoin(base_url,selected_link)
        print(final_link)
        await new_page.goto(final_link)
        await new_page.wait_for_timeout(20000)
        html_data = await cleaned_html(final_link)
        table_html_file_path = output_dir / "table_html.html"
        with open(table_html_file_path, "w", encoding="utf-8") as f:
            f.write(html_data)
        
        print("html  saved to full_html.html")
        table_data= await table_extraction(table_html_file_path)
        lists=[]
        for item in table_data:
            flat_data = item["content"]
            lists.append(flat_data)
        df=pd.DataFrame(lists)
        print("data fetched succesfully")
        print(df)
        save_path=output_dir / "table.xlsx"
        df.to_excel(save_path,index=False)   

        await browser.close()

        

# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(main())

