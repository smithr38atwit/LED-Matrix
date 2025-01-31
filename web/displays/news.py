import requests
from bs4 import BeautifulSoup

def getLatestNews():
  global message
  url = 'https://www.boston.com/tag/local-news/'

  while True:
    response = requests.get(url)
    try:
      response.raise_for_status()
    except HttpError:
      print('An error occurred')
      return

    soup = BeautifulSoup(response.content, 'html.parser')
    latest_news = soup.find('section', class_='o-featured-content')

    # Primary featured
    message = "Latest news: " + latest_news.contents[0].find_next('h3').text.strip()

    time.sleep(60)

  # Featured list
  # articles_container = latest_news.contents[1].find_next('ul')
  # for article in articles_container.children:
  #   if article == '\n':
  #     continue
  #   span = article.find_next('span', class_='js-article-card-link m-article-list__link')
  #   print(span.next.strip(), "\n")