import requests
from bs4 import BeautifulSoup
import csv,os

from scrapOneCategory import get_books_category

#function to get all books of each category
#return list of details of all books each category
def get_all_books():
   liste_livre = []
   url = "http://books.toscrape.com/"
   r = requests.get(url)
   if r.status_code != 200:
      #return error msg if name or number book is not exist
      return ["Cette page n'existe pas, veuillez réessayer"]
    soup = BeautifulSoup(r.content, "html.parser")
    menu_category = soup.find('ul',class_='nav-list')
    menu_category = menu_category.findAll('li')
    for i in range(1, len(menu_category)):
        category_href = menu_category[i].find('a')['href']
        category_href = url + category_href
        liste_livre.append(get_books_category(category_href))
    return liste_livre
  
#create csv for each category
def create_csv():
  en_tete = ["product_url", "upc", "titre", "price_incl_tax", "price_excl_tax", "number_available",
                   "product_description", "category", "reviews_rating", "image_url"]
  category_name = ""
  all_books = get_all_books_each_category()
  for i in range(len(all_books)):
      category_name = all_books[i][0][7] #to get name of category from list
      category_name = category_name.lower() #convert all char to lower
      category_name = category_name.replace(' ','-') #csv name without whitespace
      fichier = f"{category_name}-category.csv"
      # checking if the directory csv/categories exist or not.
      if not os.path.exists("csv/categories"):
          # if the csv/categories directory is not present then create it.
          os.makedirs("csv/categories")
      with open(f'csv/categories/{fichier}', 'w') as csv_file:
          writer = csv.writer(csv_file, delimiter=',')
          writer.writerow(en_tete)
          writer.writerows(all_books[i])
          
          
#run function create_csv()
try:
    if __name__ == "__main__":
      create_csv()

except Exception as e:
  print(e)
