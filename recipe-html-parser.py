from bs4 import BeautifulSoup
import os
import re
import ast
import json
  
# List that will store all of the recipe objects
recipe_list = []

# Put the directory where your recipe htmls are here
recipes_html_directory = "/Users/koudousugawara/Desktop/Code/recipe-scraper/recipe-htmls"
os.chdir(recipes_html_directory)

# Open the sitemap which contains the urls to every recipe on hellofresh
with open("sitemap_recipe_pages.xml", 'r') as f:
  contents = f.read()
  html_soup = BeautifulSoup(contents, 'html.parser')
  string_soup = str(html_soup)

  recipe_url_regex = re.compile("https:\/\/www\.hellofresh\.com\/recipes\/[a-zA-Z0-9\-]*")
  # Parse all urls from the site-map
  recipe_urls = recipe_url_regex.findall(string_soup)

# Iterate through every file in the recipes html directory
for file in os.listdir(recipes_html_directory):
  filename = os.fsdecode(file)

  if filename.endswith(".html"):
    with open(filename, 'r') as f:
      contents = f.read()
      soup = BeautifulSoup(contents, "html.parser")
      recipe_soup = soup.find(id="schema-org")
      string_soup = str(recipe_soup)
      numbers_regex = re.compile("[0-9]+")

      try:
        # Create a regular expression to find the information
        name_regex = re.compile("\"name\":\".*?\"")
        # Search the recipe using the regular expression
        name = name_regex.search(string_soup).group()
        # Clean up the data parsed
        name = name[8:-1]
      # If the info is not found then...
      except:
        name = "n/a"
        print("no name in: " + filename)

      try:
        totalTime_regex = re.compile("\"totalTime\":\".*?\"")
        totalTime = totalTime_regex.search(string_soup).group()
        # Isolate numbers and convert to an int
        totalTime = int(numbers_regex.search(totalTime).group())
      except:
        totalTime = 0
        print("no time in: " + filename)

      try:
        description_regex = re.compile("\"description\":\".*?\"")  
        description = description_regex.search(string_soup).group()
        description = description[15:-1]
      except:
        description = "n/a"
        print("no description in: " + filename)

      try:
        calories_regex = re.compile("\"calories\":\".*?\"")  
        calories = calories_regex.search(string_soup).group()
        calories = int(numbers_regex.search(calories).group())
      except:
        calories = 0
        print("no calories in: " + filename)

      try:
        fatContent_regex = re.compile("\"fatContent\":\".*?\"")  
        fatContent = fatContent_regex.search(string_soup).group()
        fatContent = int(numbers_regex.search(fatContent).group())
      except:
        fatContent = 0
        print("no fatContent in: " + filename)

      try:
        carbohydrateContent_regex = re.compile("\"carbohydrateContent\":\".*?\"")  
        carbohydrateContent = carbohydrateContent_regex.search(string_soup).group()
        carbohydrateContent = int(numbers_regex.search(carbohydrateContent).group())
      except:
        carbohydrateContent = 0
        print("no carbohydrateContent in: " + filename)

      try:
        sugarContent_regex = re.compile("\"sugarContent\":\".*?\"")  
        sugarContent = sugarContent_regex.search(string_soup).group()
        sugarContent = int(numbers_regex.search(sugarContent).group())
      except:
        sugarContent = 0
        print("no sugarContent in: " + filename)

      try:
        proteinContent_regex = re.compile("\"proteinContent\":\".*?\"")  
        proteinContent = proteinContent_regex.search(string_soup).group()
        proteinContent = int(numbers_regex.search(proteinContent).group())
      except:
        proteinContent = 0
        print("no proteinContent in: " + filename)

      try:
        recipeIngredient_regex = re.compile("\"recipeIngredient\":\[.*?\]")
        recipeIngredient = recipeIngredient_regex.search(string_soup).group()
        if recipeIngredient == "\"recipeIngredient\":[]":
          print(filename + " has an empty ingredient list")
        recipeIngredient = recipeIngredient[19:]
        # Convert the string that is formatted like a list into an actual list
        recipeIngredient = ast.literal_eval(recipeIngredient)
        # Remove ingredient amounts
        ingredient_regex = re.compile("[A-Z][^ ]*[a-z]")
        i = 0
        for ingredient in recipeIngredient:
          just_ingredient = ""
          ingredient_word_list = re.findall(ingredient_regex, ingredient)
          for word in ingredient_word_list:
            just_ingredient = just_ingredient + word + " "
          just_ingredient = just_ingredient[:-1]
          recipeIngredient[i] = just_ingredient
          i += 1
      except:
        recipeIngredient = "n/a"
        print("no recipeIngredient in" + filename)

      try:
        thumbnailUrl_regex=re.compile("\"thumbnailUrl\":\".*?\"")
        thumbnailUrl = thumbnailUrl_regex.search(string_soup).group()
        thumbnailUrl = thumbnailUrl[16:-1]
      except:
        thumbnailUrl = "n/a"
        print("no thumbnailUrl in: " + filename)

      # Search the filename for the recipe number to use as an index for the xml list
      index_regex = re.compile("[0-9]+")
      index = index_regex.search(filename).group()
      url = recipe_urls[int(index)]

      recipe = {
        "name": name,
        "description": description,
        "calories": calories,
        "carbohydrateContent": carbohydrateContent,
        "proteinContent": proteinContent,
        "fatContent": fatContent,
        "sugarContent": sugarContent,
        "recipeIngredient": recipeIngredient,
        "totalTime": totalTime,
        "thumbnailUrl": thumbnailUrl,
        "url": url
      }

      recipe_list.append(recipe)

recipes_json = json.dumps(recipe_list, indent=2)

with open("recipes.json", "w") as outfile:
  outfile.write(recipes_json)
