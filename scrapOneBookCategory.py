import requests
from bs4 import BeautifulSoup
import csv,os


from scrapOneBook import get_one_book

#function to get  books_category by parameters (string:url)
# return list of details of the book of the category in params
def get_books_category(url):
    try:
         r = requests.get(url)
         if r.status_code != 200:
             #return error msg if url doesn't work
             return ["Cette page n'existe pas, veuillez réessayer"]
         soup = BeautifulSoup(r.content, "html.parser")
         liste = soup.find('ol')
         livres = liste.find_all('article', class_='product_pod')
         next_page = soup.find('li',class_='next')
         if next_page:
             #get next page link
             next_page = next_page.find('a')['href']
         #get all books from page 1 (index)
         for livre in livres:
              link = livre.find('a')['href']
              #split the text from '/'
              link = link.split('/')
              link = link[3]
              link = link.split('_')
              if link == "":
                  return ["Ce livre n'existe pas, veuillez réessayer"]
              else:
                  book_name = link[0].replace('/','')
                  book_num = link[1]
                  liste_livre.extend(get_one_book(book_name,book_num))
         #get books from next pages
         while next_page:
            url = url.split('/')
            url = url[0]+'/'+url[1]+'/'+url[2]+'/'+url[3]+'/'+url[4]+'/'+url[5]+url[6]+'/'+next_page
            r = requests.get(url)
            if r.status_code != 200:
                # return error msg if name or number book is not exist
                return ["Cette page n'existe pas, veuillez réessayer"]
            soup = BeautifulSoup(r.content, "html.parser")
            liste = soup.find('ol')
            livres = liste.find_all('article', class_='product_pod')
            # get all books from other pages
            for livre in livres:
                link = livre.find('a')['href']
                link = link.split('/')
                link = link[3]
                link = link.split('_')
                if link == "":
                    return ["Ce livre n'existe pas, veuillez réessayer"]
                else:
                    book_name = link[0].replace('/','')
                    book_num = link[1]
                    liste_livre.append(get_one_book(url))
            next_page = soup.find('li', class_='next')
            if next_page:
                # get next page link
                next_page = next_page.find('a')['href']
         return liste_livre
    except Exception as e:
      return [e]



#create a ccv file
def create_csv(url):
    try:
     en_tete = ["product_url","upc","titre","price_incl_tax","price_excl_tax","number_available","product_description","category","reviews_rating","image_url"]
     fichier = "books_category.csv"
     # checking if the directory csv exist or not.
     if not os.path.exists("csv"):
         # if the csv directory is not present then create it.
         os.makedirs("csv")
     with open(f'csv/{fichier}', 'w') as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      writer.writerow(en_tete)
      writer.writerows(get_books_category(url))
    except Exception as e:
        return [e]

#run function create_csv()
create_csv("https://books.toscrape.com/catalogue/category/books/classics_6/index.html")
