#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init()

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve content title
    news_title = soup.find_all('div', class_='content_title')[0].text

    # Retrieve latest news paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    news_p

    # JPL Mars Space Image
    jpl_url = 'https://spaceimages-mars.com/'
    jpl_img_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'
    browser.visit(jpl_img_url)

    html = browser.html

    soup = bs(html, 'html.parser')

    # Retrieve image link
    img_path = soup.find_all('img')[0]['src']
    img_path

    # Scrape Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)
    table

    mars_facts = table[0]
    mars_facts = mars_facts.rename(columns={0: "Mars - Earth Comparison", 1: "Mars", 2: "Earth"})
    mars_facts.drop(index=mars_facts.index[0],
                    axis=0,
                    inplace=True)
    mars_facts.set_index("Mars - Earth Comparison", inplace=True)

    html_table = mars_facts.to_html()

    html_table.replace('\n', '')

    # Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Extract hemispheres item elements
    mars_hems = soup.find('div', class_='collapsible results')
    mars_item = mars_hems.find_all('div', class_='item')
    hemisphere_img_urls = []

    for i in mars_item:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text

        hems_link = hemisphere.a["href"]
        browser.visit(url + hems_link)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='wide-image-wrapper')
        image_url = image_link.find('img', class_='wide-image')['src']

        image_dict = {'title': title, 'img_url': image_url}
        hemisphere_img_urls.append(image_dict)

    print(hemisphere_img_urls)

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": img_path,
        "fact_table": table,
        "hemisphere_images": hemisphere_img_urls
    }

    browser.quit()
    return mars_dict


if __name__ == "__main__":
    print(scrape())
