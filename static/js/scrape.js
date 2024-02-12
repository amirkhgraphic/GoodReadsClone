function paginate(count, previous_url, next_url, query, currentPage) {
    statusLogger.innerHTML = 'paginating...'

    const paginationContainer = document.getElementById('pagination');
    paginationContainer.innerHTML = '';

    const totalPages = Math.ceil(count / 10);

    const paginationList = document.createElement('ul');
    paginationList.classList.add('pagination', 'justify-content-center');

    const previousPageItem = document.createElement('li');
    previousPageItem.classList.add('page-item');
    if (currentPage === 1) previousPageItem.classList.add('disabled');
    const previousPageLink = document.createElement('button');
    previousPageLink.classList.add('page-link');
    previousPageLink.onclick = () => list_books(previous_url, query, currentPage-1);
    previousPageLink.tabIndex = -1;
    previousPageLink.setAttribute('aria-disabled', currentPage === 1 ? 'true' : 'false');
    previousPageLink.innerHTML = '<span aria-hidden="true">&laquo;</span>';
    previousPageItem.appendChild(previousPageLink);
    paginationList.appendChild(previousPageItem);

    if (totalPages > 10) {
        const pages = [1, 2, 3, 4, '...', totalPages-3, totalPages-2, totalPages-1, totalPages]
        for (let i of pages) {
            const pageItem = document.createElement('li');
            pageItem.classList.add('page-item');
            if (i === parseInt(currentPage)) pageItem.classList.add('active');
            const pageLink = document.createElement('button');
            pageLink.classList.add('page-link');
            if (i !== '...') {
                pageLink.onclick = () => {
                    window.scrollTo(0, 0)
                    list_books(`${ListAPILink}${query}&page=${i}`, query, i);
                }
            }
            pageLink.innerText = i;
            pageItem.appendChild(pageLink);
            paginationList.appendChild(pageItem);
        }

    } else {
        for (let i = 1; i <= totalPages; i++) {
            const pageItem = document.createElement('li');
            pageItem.classList.add('page-item');
            if (i === parseInt(currentPage)) pageItem.classList.add('active');
            const pageLink = document.createElement('button');
            pageLink.classList.add('page-link');
            pageLink.onclick = () => {
                window.scrollTo(0, 0)
                list_books(`${ListAPILink}${query}&page=${i}`, query, i);
            }
            pageLink.innerText = i;
            pageItem.appendChild(pageLink);
            paginationList.appendChild(pageItem);
        }
    }

    const nextPageItem = document.createElement('li');
    nextPageItem.classList.add('page-item');
    if (currentPage === totalPages) nextPageItem.classList.add('disabled');
    const nextPageLink = document.createElement('a');
    nextPageLink.classList.add('page-link');
    nextPageLink.onclick = () => {
        window.scrollTo(0, 0)
        list_books(next_url, query, currentPage+1);
    }
    nextPageLink.innerHTML = '<span aria-hidden="true">&raquo;</span>';
    nextPageItem.appendChild(nextPageLink);
    paginationList.appendChild(nextPageItem);

    paginationContainer.appendChild(paginationList);
}

function fill(data, count) {
    statusLogger.innerHTML = 'Listing books...'
    document.getElementById('content').innerHTML = ''
    let results = document.getElementById('results-number')
    const container = document.getElementById('content');
    container.innerHTML = '';

    if (data.length > 0) {
        results.innerHTML = `count: ${count}`
        data.forEach(book => {
            const card = document.createElement('div');
            card.className = 'card mb-3';
            card.innerHTML = `
                <div class="row g-0">
                    <div class="col-md-4">
                        <img src="${book['image_url']}" class="img-fluid rounded-start" alt="${book['title']}" 
                             width="200px" height="300px">
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">${book['title']}</h5>
                            <p class="card-text text-muted">Author: ${book['author']}</p>
                            <p class="card-text">
                                <small class="text-muted">${book['pages']} pages, ${book['stars']}/5</small>
                                </br>
                                <small class="text-muted">Published: ${book['published_at']}</small>
                            </p>
                            <a href="/books/detail/${book['id']}" target="_blank">
                                <button class="btn btn-primary">Show detail...</button>
                            </a>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } else {
        results.innerHTML = 'Sorry! Nothing was found...'
    }
}

function list_books(url, query, currentPage) {
    statusLogger.innerHTML = 'Filtering desired books...'
    fetch(url)
        .then(response => response.json())
        .then(data => {
            paginate(data['count'], data['previous'], data['next'], query, currentPage)
            fill(data['results'], data['count'])
        })
}

const ScrapeAPILink = 'http://127.0.0.1:8000/api/scrape/?Key=';
const ListAPILink = 'http://127.0.0.1:8000/api/list/?Key=';
const searchBar = document.getElementById('search-bar');
const searchBtn = document.getElementById('search-btn');
const statusLogger = document.getElementById('status');
const pagination = document.getElementById('pagination');

function start() {
    let query = searchBar.value.trim()

    if (query === '') {
        searchBar.classList.add('is-invalid')
        return
    }

    searchBar.classList.remove('is-invalid')
    searchBtn.disabled = true;
    searchBar.disabled = true;
    statusLogger.style.display = 'block';
    statusLogger.innerHTML = 'Scraping data...'

    fetch(ScrapeAPILink + query)
        .then(response => {
            if (response.status === 200) {
                list_books(ListAPILink + query, query, 1);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Please try again');
        })
        .finally(() => {
            searchBar.disabled = false
            searchBtn.disabled = false;
            statusLogger.style.display = 'none';
        });
}

searchBtn.addEventListener(
    "click", start
);

searchBar.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        start();
    }
});