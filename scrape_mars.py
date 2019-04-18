import numpy as np
import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs 
import requests
import time
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():

    mars_data = {}
    mars_data["news_data"] = marsNewsData()
    mars_data["featured_image_url"] = marsFeaturedImageURL()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemispheres"] = marsHemisphereImageURLs()

    return mars_data


def marsNewsData():

    news_data = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    news_titles = []
    news_ps = []
    for x in range(1):

        html = browser.html
        soup = bs(html, "html.parser")

        quotes = soup.find_all("div", class_="content_title")
        pars = soup.find_all("div", class_="rollover_description")

    for quote in quotes:
        news_titles.append(quote.text)
    for par in pars:
        news_ps.append(par.text)
    news_title = news_titles[0]
    news_p = news_ps[0]

    news_data["news_title"] = news_title
    news_data["paragraph"] = news_p

    return news_data


def marsFeaturedImageURL():


    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    time.sleep(5)
 
    html_2 = browser.html
    soup_2 = bs(html_2, "html.parser")
   
    page_info = soup_2.findAll("article", {"class":["carousel_item"]})
    picture = [page.get("style") for page in page_info]
    img_url = picture[0].replace("background-image: url('","")
    img_url = img_url.replace("');","")
    featured_image_url = "https://www.jpl.nasa.gov" + img_url



    return featured_image_url

def marsWeather():


    url_3 = 'https://twitter.com/marswxreport?lang=en' 
    data = requests.get(url_3)
    time.sleep(5)

    tweet_stash = []
    html = bs(data.text, 'html.parser')
    timeline = html.select('#timeline li.stream-item')
    for tweet in timeline:
        tweet_text = tweet.select('p.tweet-text')[0].get_text()
        if "sol" in tweet_text:
            tweet_stash.append(tweet_text)
    mars_weather = tweet_stash[0]


    return mars_weather


def marsFacts():


    url_4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_4)

    mars_df = tables[0]
    mars_df.columns = ["Mars Planetary Feature", "Facts"]

    html_table = mars_df.to_html()
    html_table.replace("\n", "")
    mars_facts = html_table
 
    return mars_facts

def marsHemisphereImageURLs():


    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url_5)
    time.sleep(5)

    
    titles = []
    linklist = []
    html = browser.html
    soup = bs(html, 'html.parser')
    t = soup.find_all('h3')
    for x in t:
        titles.append(x.text)

    for i in titles:
        browser.click_link_by_partial_text(i)
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve all elements that contain book information
        u = soup.find('img', class_ = 'wide-image')
        linklist.append(base_url + u["src"])
        browser.click_link_by_partial_text('Back')

    keys  = ["title", "img_url"]
    hemisphere_image_urls = [dict(zip(keys,row)) for row in zip(titles,linklist)]


    return hemisphere_image_urls