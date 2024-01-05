# This script retrieves data from the 'TCcars' MySQL database table 'cars',
# writes it to a CSV file, reads the data using pandas,
# and writes it back to the same CSV file without an index.

import os
import mysql.connector
import pandas as pd
import csv

cnx = mysql.connector.connect(
    host='localhost',
    database='TCcars',
    user='root',
    password=''
)
cursor = cnx.cursor()

query = 'SELECT * FROM cars'
cursor.execute(query)

current_directory = os.getcwd()
file_name = os.path.join(current_directory, "cars_data.csv")

with open(file_name, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=cursor.description)
    writer.writeheader()
    for row in cursor:
        writer.writerow({k: v for k, v in zip(writer.fieldnames, row)})

df = pd.read_csv(file_name)
df.to_csv(file_name, index=False)

cursor.close()
cnx.close()