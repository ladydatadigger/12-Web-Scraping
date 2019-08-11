from bs4 import BeautifulSoup as bs 
import requests
from splinter import Browser
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    print("starting scrape", flush=True)
    browser = init_browser()

    # URL of page to be scraped NASA Mars News
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)
    print(mars_news_url, flush=True)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    print("creating beautiful soup", flush=True)
    soup = bs(html, 'html.parser')
    #Latest News Title
    news_title = soup.find('div', class_='content_title').text
    print(news_title, flush=True)
    #Paragraph text
    news_p = soup.find('div', class_="article_teaser_body").text
    print(news_p, flush=True) 
    

    # Look for featured image in JPL Featured Space
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    #click FULL IMAGE
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    #click more info
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    browser.click_link_by_partial_text('.jpg')
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    img_mars = soup.find('img')
    featured_image_url = img_mars.get('src')
    # print(featured_image_url)
    

    #Look for latest tweet on Mars Weather twitter account
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    mars_weather= soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    # print(mars_weather)
    

    #Look for Mars Facts
    facts_url="https://space-facts.com/mars/"
    tables = pd.read_html(facts_url, header=None)
    # type(tables)
    df = tables[1]
    df.columns=["Description", "Value"]
    df =df.set_index("Description")
    html_table = df.to_html()
    # html_table.replace('\n', '')
    # print(html_table)
    

    # Look for url to Mars Hemispheres  and high resolution images
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    #save both image url string for full resolution hemisphere image
    #save Hemisphere title containining hemisphere name
    #in a python dictionary
    hemisphere_image_urls =[]

    links = soup.find_all("div", class_="item")
    base_url = 'https://astrogeology.usgs.gov'
    for link in links:
        title = link.find('h3').text
        title = title.replace("Enhanced","")
        get_image_url = link.find('div', class_='description').a['href']
        full_image_url = base_url + get_image_url
        browser.visit(full_image_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find('div', class_='downloads').a['href']

        hem_dict = {'title': title, 'img_url':img_url}
        hemisphere_image_urls.append(hem_dict)    

    # print(hemisphere_image_urls)
    
    #mars data we can insert into mongo
    mars_data= {
        "news_title":news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    browser.quit()
    return mars_data
