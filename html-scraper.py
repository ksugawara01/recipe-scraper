from bs4 import BeautifulSoup
import requests
import os
import re
import time

# Put the directory you want to save the recipe htmls to here (also place the sitemap in this directory)
recipes_html_directory = '/Users/koudousugawara/Desktop/Code/recipe-scraper/recipe-htmls'
os.chdir(recipes_html_directory)

# Open the sitemap which contains the urls to every recipe on hellofresh
with open("sitemap_recipe_pages.xml", 'r') as f:
  contents = f.read()
  soup = BeautifulSoup(contents, 'html.parser')
  string_soup = str(soup)

  recipe_url_regex = re.compile("https:\/\/www\.hellofresh\.com\/recipes\/[a-zA-Z0-9\-]*")
  # Parse all urls from the site-map
  recipe_urls = recipe_url_regex.findall(string_soup)

  i = 0

  # Iterate through urls
  for url in recipe_urls:
    recipeHTML = requests.get(url)
    recipe_soup = BeautifulSoup(recipeHTML.text, 'html.parser')
    # Create the name of the html file
    fileName = "recipe" + str(i) + ".html"
    Func = open(fileName, "w")
    Func.write(str(recipe_soup))
    Func.close()
    print("Scraped recipe #" + str(i))
    i = i + 1
    # Suspend for 10 seconds so that you don't spam the servers with requests
    time.sleep(10)

  print("finished")
