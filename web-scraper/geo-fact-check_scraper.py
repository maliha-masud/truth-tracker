import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_article_info_selenium(article_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(article_url)

    try:
        #wait for article to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'long-content')))

        #Extract required article information
        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = article_soup.find('div', class_='long-content main').find('h1').text.strip()

        #Extract all paragraphs from the div excerpt-full
        text_paragraphs = article_soup.find('div', class_='excerpt-full').find_all('p')
        text = ' '.join(paragraph.text.strip() for paragraph in text_paragraphs)

        #Extract date with time
        date_str = article_soup.find('div', class_='time-section').find('p', class_='post-date-time').find('span').text.strip()
        article_date = pd.to_datetime(date_str, format='%A %b %d, %Y')

        #Extract Claimant Content
        claimant_content_paragraphs = article_soup.find('div', class_='story-detail').find_all('p')
        claimant_content = ' '.join(paragraph.text.strip() for paragraph in claimant_content_paragraphs)

        #Extract Textual Rating
        textual_rating_start = "The claim is"
        if textual_rating_start in claimant_content:
            textual_rating_idx = claimant_content.find(textual_rating_start) + len(textual_rating_start)
            next_word = claimant_content[textual_rating_idx:].split()[0].capitalize()
        else:
            next_word = ''

        #Extract Author
        author_start = "With additional reporting by"
        if author_start in claimant_content:
            author_idx = claimant_content.find(author_start) + len(author_start)
            #extract words until the full stop, excluding unwanted words
            unwanted_words = ["Follow", "us", "on", "@GeoFactCheck.", "If", "our", "readers", "detect", "any",
                              "errors,", "we", "encourage", "them", "to", "contact", "us", "at", "geofactcheck@geo.tv"]
            author_words = [word.capitalize() for word in claimant_content[author_idx:].split() if
                            '.' not in word and word not in unwanted_words]
            author = ' '.join(author_words)
        else:
            author = ''

        return {
            'Title': title,
            'Text': text,
            'Date': article_date,
            'Publisher Site': 'https://www.geo.tv/category/geo-fact-check',
            'Publisher Name': 'Geo Fact-Check',
            'Published At': 'Geo News',
            'Claimant Content': claimant_content,
            'Textual Rating': next_word.strip('.'),
            'Author': author
        }

    except Exception as e:
        print(f"An error occurred while extracting article information: {e}")

    finally:
        driver.quit()

    return None

#extract article URLs from the main page using Selenium
def extract_article_urls_selenium(main_page_url, start_date, end_date):
    article_urls = []
    current_page = 1  #initialize current_page

    #set up the Selenium webdriver
    driver = webdriver.Chrome()
    driver.get(main_page_url)

    try:
        while True:
            #scroll down to trigger dynamic loading
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)  # Adjust sleep time as needed

            #wait for new content to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))

            #extract article URLs
            main_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            for card in main_page_soup.find_all('div', class_='card h-100'):
                date_str = card.find('span', class_='date').text.strip()
                article_date = pd.to_datetime(date_str + ' ' + str(pd.to_datetime('today').year), errors='coerce')

                if pd.notna(article_date) and start_date <= article_date <= end_date:
                    article_url = card.find('a', class_='text-body')['href']
                    article_info = extract_article_info_selenium(article_url)

                    if article_info:
                        #add URL and Date to the article information
                        article_info.update({'URL': article_url, 'Date': article_date})
                        article_urls.append(article_info)

                elif article_date < start_date:
                    # if the date is out of the required range, stop fetching more articles
                    return article_urls

            #check if there are more pages
            load_more_button = main_page_soup.find('button', class_='btn btn-primary mb-0 load_more_fact_news')
            if load_more_button:
                current_page += 1
            else:
                break
    except Exception as e:
        print(f"An error occurred while extracting article URLs: {e}")
    finally:
        driver.quit()

    return article_urls

#set the main page URL & date range
main_page_url = 'https://www.geo.tv/category/geo-fact-check'
start_date = pd.to_datetime('2022-8-30')
end_date = pd.to_datetime('2023-10-14')

#extract article information using Selenium
article_info_list = extract_article_urls_selenium(main_page_url, start_date, end_date)

#save article information to Excel file
df_article_info = pd.DataFrame(article_info_list)
df_article_info['Date'] = df_article_info['Date'].dt.strftime('%Y-%m-%d')
df_article_info.to_excel('geo_fact_check_article_info.xlsx', index=False)