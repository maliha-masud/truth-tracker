import requests  # HTTP client library. can easily send and receive information over the internet, using HTTP protocol
from bs4 import BeautifulSoup  # package for parsing HTML and XML documents. create parse tree for parsed pages to extract data from HTML
from datetime import datetime, timedelta  # timedelta: calculating differences in dates and times
import pandas as pd  # data manipulation and analysis
import re  # regular expression facilities can check if a string matches a pattern (match function), or contains a pattern (search function)

# the order of columns in which to store data {corresponds to the columns in original PK dataset}
column_order = [
    "URL", "Title", "Text", "Review Date", "Textual Rating", "Publisher Site", "Publisher Name",
    "Claim Date", "Claimant", "Content", "Published At", "Author", "Url to Image"
]

# format of URLs on the site: "https://dependent.pakistantoday.com.pk"/{YYYY/MM/DD}/some-post-name/
base_url = "https://dependent.pakistantoday.com.pk/"
start_date = datetime(2019, 9, 1)
end_date = datetime(2019, 11, 30)

# the file in which to store the scraped content
existing_file_path = "pakistani_dataset_consolidated_augmented.xlsx"


def convert_URL_to_Date(url):
    """Return the date of an article, given its URL.

    >>> convert_URL_to_Date(https://dependent.pakistantoday.com.pk/2020/07/05/uk-minister-says-.../)
    2020-07-05
    """

    # extract date segments from URL
    date_str = url.split("/")[3:6]  # starting at the 3rd slash of the URL, ending at the 6th: list of elements

    # create date string, in the form YYYY/MM/DD; join the "list" of elements
    date_str = "/".join(date_str)

    # return as required format for dataset: YYYY-MM-DD
    date_obj = datetime.strptime(date_str, "%Y/%m/%d")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


# dataframe to store data; column order specified
result_df = pd.DataFrame(columns=column_order)


def generate_article_urls(base_url, start_date, end_date):
    """Generate and return all the URLs posted on a given date range
    with the help of regular expressions.

    >>> generate_article_urls(https://dependent.pakistantoday.com.pk/, 2023-12-01, 2023-12-31)
    https://dependent.pakistantoday.com.pk/2023/03/01/not-my-supreme-court-says-maryam-insisting-elections-to-only-happen-when-she-says-so/
    https://dependent.pakistantoday.com.pk/2023/06/20/it-was-all-just-a-dream-imran-realises-after-waking-up-on-container-in-2014/
    ...
    """

    current_date = start_date
    article_urls = []  # store all URLs generated
    while current_date <= end_date:  # iterate through the dates
        date_str = current_date.strftime("%Y/%m/%d")  # "string from time" function
        article_pattern = re.compile(
            f"{date_str}/(.*?)/")  # using RE for pattern match - does it have the date, followed by any text
        response = requests.get(f"{base_url}{date_str}")  # get response object for a URL
        if response.status_code == 200:  # successful; ok
            soup = BeautifulSoup(response.text,
                                 "html.parser")  # extract text from HTML element ("parse": divide into components)
            # extract all URLs that match criteria
            for link in soup.find_all('a'):  # locate all occurrences of element "a" in a document
                href = link.get('href')
                if isinstance(href, str):  # is href a string
                    match = article_pattern.search(href)  # use previously created re to find matching URLs
                    if match:
                        article_url = f"{base_url}{date_str}/{match.group(1)}/"  # construct URL
                        article_urls.append(article_url)  # add to list
        current_date += timedelta(days=1)  # increment to next day
    return article_urls


def scrape_article_content(article_url):
    """Scrape the content of an article, given its URL.

    >>> scrape_article_content(https://dependent.pakistantoday.com.pk/2020/02/21/pakistan-auto-show-draws-25000-customers-on-first-day/)
    >>> (Found in <div class="td_block_wrap tdb_single_content tdi_64 td-pb-border-top td_block_template_1 td-post-content tagdiv-type" data-td-block-uid="tdi_64">)
    >>> (in div class="tdb-block-inner td-fix-index", divided into multiple <p> elements)
    The three-day Pakistan Auto Show 2020 (PAS20) kicked off at ...
    ...
    """

    # navigate to the URL
    response = requests.get(article_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # extract and store title (the only h1 in the page)
        if soup.find("h1.text"):
            article_title = soup.find("h1").text
        else:
            article_title = ""  # in case nothing found to store in title

        # -------------- extraction of text & content --------------

        # found in following div class:
        outer_div = soup.find("div", {
            "class": "td_block_wrap tdb_single_content tdi_64 td-pb-border-top td_block_template_1 td-post-content tagdiv-type",
            "data-td-block-uid": "tdi_64"})
        if not outer_div:  # error check
            outer_div = soup.find("div", {
                "class:" "td_block_wrap tdb_single_content tdi_64 td-pb-border-top td_block_template_1 td-post-content tagdiv-type"})

        # found in the inner <div>, class "tdb-block-inner td-fix-index"
        if outer_div:
            inner_div = outer_div.find("div", class_="tdb-block-inner td-fix-index")
        else:
            return

        # find all <p> elements in the div
        paragraphs = inner_div.find_all("p")

        if paragraphs:
            # store first <p> separately; to be stored as text
            first_paragraph_text = paragraphs[0].text

            # extract rest of the <p> elements; to be stored as content
            rest_of_paragraphs_text = "\n".join(paragraph.text for paragraph in paragraphs[1:])

        else:  # <p> elements not found: nothing to scrape
            return

        # -------------- end of extraction of text & content --------------

        # create dictionary with required information, in required order
        data = {
            "URL": article_url,
            "Title": article_title,
            "Text": first_paragraph_text,
            "Review Date": convert_URL_to_Date(article_url),
            "Textual Rating": "Satire",
            "Publisher Site": "https://dependent.pakistantoday.com.pk/",
            "Publisher Name": "The Dependent by PT Pakistan Today",
            "Claim Date": convert_URL_to_Date(article_url),
            "Claimant": "The Dependent",
            "Content": rest_of_paragraphs_text,  # Just the article text, excluding the first paragraph
            "Published At": convert_URL_to_Date(article_url),
            "Author": "The Dependent",
            "Url to Image": ""
        }

        return data
    else:  # response other than 200
        print(f"Failed to retrieve {article_url}")
        return None


# --------------- main ---------------
# generate articles using function
article_urls = generate_article_urls(base_url, start_date, end_date)
# scrape every generated article
for article_url in article_urls:
    article_data = scrape_article_content(article_url)
    if article_data:  # store scraped content in the dataframe to store data
        result_df = pd.concat([result_df, pd.DataFrame(article_data, index=[0])], ignore_index=True)

# -- appending the excel file --
# read the existing file
df_existing = pd.read_excel(existing_file_path)

# concat existing file with scraped data
combined_df = pd.concat([df_existing, result_df], ignore_index=True)  # without preserving the original index values

# replace original file with appended one
combined_df.to_excel(existing_file_path, index=False, columns=column_order)  # don't include index values
