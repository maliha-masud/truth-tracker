# meter-mostly-true, meter-false, meter-half-true, tom_ruling_pof, meter-mostly-false, meter-true
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

base_url = "https://www.politifact.com/search/factcheck/?page={}&q=pakistan"

# the order of columns in which to store data {corresponds to the columns in original PK dataset}
column_order = [
    "URL", "Title", "Text", "Review Date", "Textual Rating", "Publisher Site", "Publisher Name",
    "Claim Date", "Claimant", "Content", "Published At", "Author", "Url to Image"
]

# the file in which to store the scraped content
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"

# dataframe to store data; column order specified
result_df = pd.DataFrame(columns=column_order)

date_format = "%B %d, %Y"  # date format, e.g. April 21, 2023
cutoff_date = datetime(2021, 1, 1)  # date after which to scrape

# dictionary to map extracted image values to desired output
value_mapping = {
    "meter-false": "False",
    "tom_ruling_pof": "False",
    "meter-mostly-false": "Mostly False"
}

# iterate through pages with the query "pakistan"
for page_number in range(2, 37):  # there are 36 pages
    url = base_url.format(page_number)

    response = requests.get(url)  # send HTTP GET request to the URL

    if response.status_code == 200:  # successful request
        soup = BeautifulSoup(response.text, "html.parser")
        # extract <div> elements with class "o-listease__item"
        fact_items = soup.find_all("div", class_="o-listease__item")

        # iterate through each fact item
        for fact_item in fact_items:
            title_section = fact_item.find("div", class_="c-textgroup__title")
            if title_section:  # check for title section
                # extract URL link
                link = title_section.find("a", href=True)["href"]
                title = title_section.find("a").text

                # find author details of fact_item
                author_section = fact_item.find("div", class_="c-textgroup__meta")
                author_text = author_section.get_text()

                # extract only the author's name from: By Loreben Tuquero • April 21, 2023
                og_author_name = author_text.split("•")[0].strip()  # split with • part, get 1st part
                author_name = og_author_name.replace("By", "").strip()

                # extract part with date
                date_text = author_text.split("•")[-1].strip()  # split with • part, get 2nd part
                date = datetime.strptime(date_text, date_format)

                if date > cutoff_date:
                    # find the claimant information
                    claimant = fact_item.find("div", class_="c-textgroup__author").find("a").text

                    # find image in the HTML, as it has rating of image
                    media_section = fact_item.find("div", class_="m-result__media")
                    img_src = media_section.find("img")["src"]

                    # extract only the ruling from the image URL
                    # e.g. https://static.politifact.com/CACHE/images/politifact/rulings/meter-mostly-false/df2fdc0878a20d18f0ed2f059e16b858.jpg
                    # mostly false
                    ruling = \
                        img_src.split("https://static.politifact.com/CACHE/images/politifact/rulings/")[1].split("/")[0]

                    if ruling not in ["meter-mostly-true", "meter-half-true", "meter-true"]:
                        # map extracted ruling to storable output
                        mapped_ruling = value_mapping.get(ruling)

                        # create dictionary with required information, in required order
                        data = {
                            "URL": "https://www.politifact" + link,
                            "Title": title,
                            "Text": title,
                            "Review Date": date.strftime('%Y-%m-%d'),
                            "Textual Rating": mapped_ruling,
                            "Publisher Site": "https://www.politifact.com",
                            "Publisher Name": "Politifact",
                            "Claim Date": date.strftime('%Y-%m-%d'),
                            "Claimant": claimant,
                            "Content": "",
                            "Published At": date.strftime('%Y-%m-%d'),
                            "Author": author_name,
                            "Url to Image": ""
                        }
                    result_df = pd.concat([result_df, pd.DataFrame(data, index=[0])], ignore_index=True)

    else:
        print(f"Failed to retrieve {page_number}.")

# -- appending the excel file --
# read the existing file
df_existing = pd.read_excel(existing_file_path)

# concat existing file with scraped data
combined_df = pd.concat([df_existing, result_df], ignore_index=True)

# replace original file with appended one
combined_df.to_excel(existing_file_path, index=False, columns=column_order)
