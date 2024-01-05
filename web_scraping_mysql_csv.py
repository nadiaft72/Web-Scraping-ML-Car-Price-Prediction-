from bs4 import BeautifulSoup
import csv
import mysql.connector
import numpy as np
import pandas as pd
import re
import requests
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import os

# Connect to the MySQL database 'TCcars'.
cnx = mysql.connector.connect(
    host='localhost',
    database='TCcars',
    user='root',
    password=''
)
cursor = cnx.cursor()

num_pages = 5
car_model_name = car_model = car_mileage = car_accident = car_location = car_year = ""
car_dict = dict()
car_list = list()

# Scraping data from web pages.
for page_num in range(1, num_pages):
    url = f"https://www.truecar.com/used-cars-for-sale/listings/acura/?page={page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    car_elements = soup.find_all("div", attrs={"class": "card-content vehicle-card-body order-3"})

    for car in car_elements:
        car_top = car.find("div", attrs={"class": "vehicle-card-top"})
        header = car_top.find("div", attrs={"class": "vehicle-card-header w-100"}).text.split()
        car_year = header[0]
        car_model_name = header[1]

        info_truncate = car_top.find("div", attrs={"class": "font-size-1 text-truncate"}).text.split()
        car_model = info_truncate[0]

        car_location_div = car.find("div", attrs={"class": "margin-top-2_5 padding-top-2_5 border-top w-100"})
        location_text = car_location_div.find("div", attrs={"class": "font-size-1 text-truncate"}).text.split()
        car_mileage = int(re.sub(r',', '', str(location_text[0])))

        location = car_location_div.find("div", attrs={"class": "vehicle-card-location font-size-1 margin-top-1"}).text.split()
        car_location = location[-1]

        condition = car.find("div", attrs={"class": "vehicle-card-location font-size-1 margin-top-1", "data-test": "vehicleCardCondition"}).text.split()
        car_accident = condition[0]

        bottom_info = car.find("div", attrs={"class": "vehicle-card-bottom vehicle-card-bottom-top-spacing"})
        price_text = bottom_info.find("div", attrs={"class": "padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50"}).text.split()
        car_price = int(re.sub(r',', '', price_text[0][1:]))

        car_details = {"model_name": car_model_name, "model": car_model, "mileage": car_mileage, "accident": car_accident, "location": car_location, "year": car_year, "price": car_price}
        car_list.append(car_details)

# Add scraped data to the MySQL database table 'cars'.
cursor.executemany("""
    INSERT INTO cars (model_name,model,mile,accident,location,year,price)
    VALUES (%(model_name)s, %(model)s ,%(mile)s,%(accident)s,%(location)s,%(year)s,%(price)s)""", car_list)
cnx.commit()

query = 'SELECT * FROM cars'
cursor.execute(query)

current_directory = os.getcwd()
file_name = os.path.join(current_directory, "cars_data.csv")

# Write the fetched data to the 'cars_data.csv' CSV file.
with open(file_name, "w") as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(col[0] for col in cursor.description)
    for row in cursor:
        if row:
            writer.writerow(row)

df = pd.read_csv(file_name)
df.to_csv(file_name, index=False)

print("Data has been added to cars_data.csv. You can now run MLexp.py.")