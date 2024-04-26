from selenium import webdriver
from bs4 import BeautifulSoup
import psycopg2

def insert_data(nome,rating,comentario):
    conn = psycopg2.connect(
        dbname="restaurantes",
        user="postgres",
        password="admin",
        host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (nome, rating, comentario) VALUES (%s, %s,  %s)", (nome, rating, comentario))
    conn.commit()
    cursor.close()
    conn.close()

url = "https://www.google.com/maps/place/Nema/@-22.9841517,-43.2128543,15z/data=!3m1!5s0x9bd50757e02857:0x35aa6a9b37f5d532!4m8!3m7!1s0x9bd58a0cdc1487:0x4c1eb56d62eb469b!8m2!3d-22.9841517!4d-43.2128543!9m1!1b1!16s%2Fg%2F11j20tdp78?entry=ttu"
driver = webdriver.Chrome()

driver.get(url)

driver.implicitly_wait(10)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

reviews = soup.find_all('div', class_='jJc9Ad')

for review in reviews:
    nome_element = review.find('div', class_='d4r55')
    nome = nome_element.text.strip() if nome_element else "Nome não encontrado"

    rating_element = review.find('span', class_='kvMYJc')
    rating = rating_element['aria-label'] if rating_element else "Rating not found"
    comentario = review.find('span', class_='wiI7pd').text.strip() if review.find('span', class_='wiI7pd') else "Comentário não encontrado"

    insert_data(nome, rating, comentario)

    print("Nome do review:", nome)
    print("Rating:", rating)
    print("Comentário:", comentario)

driver.quit()
