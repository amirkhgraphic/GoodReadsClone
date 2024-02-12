from typing import TypedDict
from datetime import datetime, date
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import scraper_settings
import logging

# Create and Config logger
logging.basicConfig(
    format='%(levelname)s - (%(asctime)s) - %(message)s - (Line: %(lineno)d) - [%(filename)s]',
    datefmt='%H:%M:%S',
    encoding='utf-8',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Book(TypedDict):
    title: str | None
    author: str | None
    stars: float
    description: str
    genres: list[tuple[str, str]]
    pages: int | None
    published_at: date | None
    image_url: str | list[str] | None


def to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%B %d, %Y').date()


async def fetch(session, url):
    logger.info(f'fetch url... {url}')
    async with session.get(url) as response:
        return await response.text()


async def scrape_page(session, query: str, page_number: int) -> list[Book]:
    url = scraper_settings.URL.format(page=page_number, query=query)

    response_text = await fetch(session, url)
    soup = BeautifulSoup(response_text, 'lxml')

    try:
        results = soup.select_one('h3.searchSubNavContainer')
        if results.string == 'No results.':
            return []
    except AttributeError:
        logger.warning('can not check... restart server !!!')

    books = []
    tbody = soup.select_one('table.tableList')
    for tr in tbody.select('tr'):
        try:
            book: Book = {}
            url = 'https://www.goodreads.com' + tr.select_one('a').get('href')
            response_text = await fetch(session, url)
            soup = BeautifulSoup(response_text, 'lxml')

            title = soup.select_one('h1', {'data-testid': 'bookTitle'})
            book['title'] = title.string

            author = soup.select_one('span.ContributorLink__name')
            book['author'] = author.string

            stars = soup.select_one('div.RatingStatistics__rating')
            book['stars'] = float(stars.string)

            tags = soup.select_one('span.Formatted')
            book['description'] = "\n".join([str(tag) for tag in tags.contents])

            genres = soup.select('span.BookPageMetadataSection__genreButton')
            book['genres'] = []
            for genre_tag in genres:
                book['genres'].append((genre_tag.string, genre_tag.find('a').get('href')))

            try:
                pp = soup.select_one('div.FeaturedDetails')
                page, published_at = pp.select('p')
                try:
                    book['pages'] = int(page.string.split()[0])
                except ValueError:
                    book['pages'] = None

                book['published_at'] = to_date(' '.join(published_at.string.split()[-3:]))

            except ValueError:
                book['pages'] = None
                book['published_at'] = None

            except AttributeError:
                book['pages'] = None
                book['published_at'] = None
                logger.warning('connection is weak :( \nrestart the server')

            img = soup.select_one('img.ResponsiveImage', {'role': 'presentation'})
            book['image_url'] = img.get('src')

            books.append(book)

        except:
            logger.info('missed one item :_(')

    return books


async def scrape(query: str):
    books = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, query, i+1) for i in range(5)]
        results = await asyncio.gather(*tasks)
        for book in results:
            books.extend(book)
    logger.info('done!')
    return books


if __name__ == '__main__':
    bs = asyncio.run(scrape('batman'))
    for b in bs:
        print(b['title'])
    print(len(bs))
