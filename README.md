# Money Stretcher

![main image](https://github.com/jqpoon/ichelloworld-2021/blob/main/flask/static/assets/img/github_cover.jpg)

## Inspiration 
With the ongoing COVID pandemic, it is much more safe and socially responsible to do our shopping online. At the same time, the economic impact of the virus had impacted many households and it is more important than ever to save money when we can . The nature of online shopping makes it easy for us to buy different products from different places but people lack a centralised avenue to compare prices for a given product. We hope that our web service can help people stretch every penny to help overcome this trying time. 

## What we learnt 
Through this project, we became more familiar with using different tools and frameworks such as BootStrap for the front end, Selenium for web scraping and Flask for integration. We had to learn how to build a website using flask as well as how to handle querying a database and passing the information to the view. We also learnt how to decipher source code and use BeautifulSoup to extract the specific data that we needed for our project (price, item name etc).   

## Challenges faced 
We ran into some difficulty scraping UK supermarket sites using BeautifulSoup as if we use request.get the website is loaded after that request is sent, making us unable to scape the data we need. When using Selenium, the script is also limited by the user's internet speed, and one possibility is that the code runs ahead before the webpage in the background is loaded. This throws unexpected errors and does not allow for data to be scraped. Another possibility is that the product displayed on the supermarket's pages are sold out, which again throws errors as the information we are looking for is unavailable.

When trying to order based on price, we also ran into challenges as the price was represented as a string after scraping thus ordering it by price leads to some unexpected behaviour.

## Future Extensions 
Given more time, we would like to expand our database to include data from more supermarkets as well as add some kind of filtering so that it is easier for users to get the results they want.  
