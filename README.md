# GoodReadsClone (Django/BeautifulSoup4) 🌐

## Description 📑
this is a django project; this project is consist of some major parts. `API` app, which is the api that is developed 
using `django-rest-framework` and all javascript parts are using these APIs to read posts from database and list them.
After that there is the `book` app; this app is for getting user's input for scraping related books. Then we have the 
`scraper.py`; which is the main script for scraper that is developed using `bs4` and `requests`. this is 
where user's input is sent to and then retrieved scraped data and save them if not already exists. 


## How to Run ❓
first you need to create a virtual environment, cd to the directory where this file is and then run the following command:

Create and Activate a Virtual Environment:

- Linux/mac: 
```bash
$ pip install virtualenv
$ virtualenv [YourVenvName]
$ source [YourVenvName]/bin/activate
```

- Windows:
```cmd
pip install virtualenv
python -m venv [YourVenvName]
[YourVenvName]/Scripts/activate
```
<br>

install the required libraries and run the code:
```bash
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Contribute! 🤝🏻
I'm more than happy to hear your feedbacks and collaborate with you guys!

if you had any problem contributing on the project, feel free to contact me:

- [Gmail](mailto:amirhosseinkhalili901@gmail.com "my gmail address")
- [LinkedIn](https://linkedin.com/in/amirhossein-khalili-a83250271 "my LinkedIn account")
- [Telegram](https://t.me/Amirkh_MoD "my Telegram account")
- [Github](https://github.com/amirkhgraphic "my Github account")
- [Quera](https://quera.org/profile/Amirkh1996 "my Quera profile/resume")


*- Amirhoseein Khalili*