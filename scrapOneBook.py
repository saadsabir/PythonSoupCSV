import requests
from bs4 import BeautifulSoup
import csv, os, urllib.request

#function to get one book by parameters (string:url)
#return list of details of the book
def get_one_book(url):
     try:
        liste_livre = []
        r = requests.get(url)
        if r.status_code!=200:
            #return error msg if url doesn't work
            return ["Cette page n'existe pas, veuillez réessayer"]
        soup = BeautifulSoup(r.content, "html.parser")
        product_url =url
        image = soup.find('img')
        image_url = image.attrs['src']
        full_image_url = ""
        image_url = image_url[6:]  # remove first 6 char using python slicing
        full_image_url = "http://books.toscrape.com/"+image_url
        titre = image.attrs['alt']
        product_description=soup.findAll('p')[3].text
        product_description=product_description.replace('\n','')
        category =soup.findAll('a')[3].text
        table = soup.findAll('table')[0]
        rows = table.findAll('tr')
        upc = table.findAll('td')[0].text
        product_type=table.findAll('td')[1].text
        price_excl_tax = table.findAll('td')[2].text
        price_incl_tax = table.findAll('td')[3].text
        tax =table.findAll('td')[4].text
        number_available = table.findAll('td')[5].text
        number_available = number_available.split('(')
        number_available = number_available[1]
        number_available = number_available.split(' ')
        number_available = number_available[0]
        reviews_rating = soup.find('p',class_='star-rating')
        reviews_rating = reviews_rating['class'][1]
        if reviews_rating == 'One':
           reviews_rating = 1
        elif reviews_rating == 'Two':
           reviews_rating = 2
        elif reviews_rating == 'Three':
           reviews_rating = 3
        elif reviews_rating == 'Four':
           reviews_rating = 4
        elif reviews_rating == 'Five':
           reviews_rating = 5
               
        #get image of book
        image_name = product_url.split('/')
        image_name = image_name[4]
        image_name = image_name+".jpg"
        path = f'images/{category}'

        # checking if the directory images/x exist or not.
        if not os.path.exists(path):
            # if the images/x directory is not present then create it.
            os.makedirs(path)
        #download image
        urllib.request.urlretrieve(full_image_url,path+'/'+image_name)

        return [product_url,upc,titre,price_incl_tax,price_excl_tax,number_available,product_description,category,reviews_rating,full_image_url]
     except Exception as e:
             return [e]


#create a ccv file
def create_csv(url):
en_tete = ["product_url","upc","titre","price_incl_tax","price_excl_tax","number_available","product_description","category","reviews_rating","image_url"]
fichier = "one_book.csv"
# checking if the directory csv exist or not.
if not os.path.exists("csv"):
    # if the csv directory is not present then create it.
    os.makedirs("csv")
with open(f'csv/{fichier}', 'w') as csv_file:
 writer = csv.writer(csv_file, delimiter=',')
 writer.writerow(en_tete)
 writer.writerow(get_one_book(url))


#run function create_csv
try :
  if __name__ == "__main__":
    create_csv("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
except Exception as e:
  print(e)
