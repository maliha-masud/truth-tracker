import time
import pandas as pd
import string
from bs4 import BeautifulSoup
from selenium import webdriver

#extract article information from the article URL using Selenium
def extract_article_info_selenium(article_card):
    try:
        #Extract text from "Claim text"
        text = article_card.find('div', class_='fc-claim').text.strip()

        #Extract claimant text
        claimant_element = article_card.find('div', class_='fc-claimer-name')
        claimant_text = claimant_element.text.split("Claim by")[-1].strip().rstrip(':').strip()

        #Remove punctuation only from the end of claimant text
        claimant = claimant_text.rstrip(string.punctuation)

        #Extract publisher and textual rating
        publisher_info = article_card.find('span', class_='fc-review-publisher')
        if publisher_info:
            publisher = publisher_info.find('span', class_='fc-google-sans-md').text.strip()
            textual_rating = publisher_info.find('span', class_='ng-tns-c866644945-3 fc-google-sans-md').text.strip()
        else:
            publisher = ''
            textual_rating = ''

        #Extract URL
        url_element = article_card.find('div', class_='fc-viewarticle').find('a')
        url = url_element['href'] if url_element else ''

        #Extract title text
        title_text = url_element.get('title', '')
        title = title_text.strip() if title_text else ''

        #Extract date
        date_element = article_card.find('div', class_='fc-inline-block fc-label ng-tns-c866644945-3 ng-star-inserted')
        date_str = date_element.text.strip()
        date = pd.to_datetime(date_str + ' ' + str(pd.to_datetime('today').year), errors='coerce')

        return {
            'URL': url,
            'Title': title,
            'Text': text,
            'Review Date': date.strftime('%Y-%m-%d') if not pd.isna(date) else None,
            'Textual Rating': textual_rating,
            'Publisher Site': '',
            'Publisher Name': publisher,
            'Claim Date': date.strftime('%Y-%m-%d') if not pd.isna(date) else None,
            'Claimant': claimant,
            'Content': '',
            'Published At': 'Fact Check Explorer',
            'Author': '',
            'Url to Image': ''
        }

    except Exception as e:
        print(f"An error occurred while extracting article information: {e}")
        return None

#extract article URLs from the main page using Selenium
def extract_article_urls_selenium(main_page_url, max_articles=980):
    article_info_list = []
    articles_scraped = 0

    #Set up the Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(main_page_url)

    try:
        #scroll to the bottom to load more articles
        last_height = driver.execute_script("return document.body.scrollHeight")

        while articles_scraped < max_articles:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  #adjust sleep time as needed

            #Extract article cards
            main_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            article_cards = main_page_soup.find_all('div', class_='fc-card-content ng-tns-c866644945-3')

            for card in article_cards:
                article_info = extract_article_info_selenium(card)

                if article_info:
                    article_info_list.append(article_info)
                    articles_scraped += 1

                    if articles_scraped == max_articles:
                        break

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except Exception as e:
        print(f"An error occurred while extracting article information: {e}")
    finally:
        driver.quit()

    return article_info_list

#set the main page URL
main_page_url = 'https://toolbox.google.com/factcheck/explorer/search/pakistan;hl=en'

#extract article information using Selenium
article_info_list = extract_article_urls_selenium(main_page_url, max_articles=1000)

#Save the article information to Excel file
df_article_info = pd.DataFrame(article_info_list)
df_article_info.to_excel('google_fact_check_article_info.xlsx', index=False)
