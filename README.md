# AmazonScraper
Scrapes all books over [Amazon] (https://www.amazon.in) 
Refer to **requirements.txt** for dependencies.
We used scrapy framework to make our working smooth here. 
**Scrapy** is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival.

Installation Guide for Linux Users:
To Install Scrapy:
* pip install Scrapy // install scrapy using pip
* scrapy createproject Amazon // creating project
* cd Amazon // go to the project directory
* scrapy genspider amazon amazon.in // generate your spider and provide allowed domains to be scraped by your spider

I would highly recommend you to use virtual environment while working on your project.
To install virtual env on linux machine 
> pip install virtualenv

Know more details about [virtualenv] (https://virtualenv.pypa.io/en/stable/installation/)
