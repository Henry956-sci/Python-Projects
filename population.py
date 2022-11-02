import math
import random
import mysql
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

#connects to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="test",
  password="test"
)

print(mydb)

mycursor = mydb.cursor()

#creates the database if it doesn't exist, creates a table of the top 10 populated countries of the world
mycursor.execute("CREATE DATABASE IF NOT EXISTS myPop")
mycursor.execute("CREATE TABLE IF NOT EXISTS myPop.topTen SELECT Name, Population, Code FROM world.country ORDER BY Population DESC LIMIT 10")
mycursor.execute("CREATE TABLE IF NOT EXISTS myLang.topTen SELECT Language FROM world.countrylanguage WHERE CountryCode = myPop.topTen.Code")



#gets the total population of the world
mycursor.execute("SELECT SUM(population) FROM world.country")
result = mycursor.fetchone()
totalPop = result[0]
print(totalPop)

#creates a list out of the top 10 populated countries in the world
mycursor.execute("SELECT * FROM mypop.topten")
result = mycursor.fetchall()

for x in result:
    print(x)

#gets the name of the countries, and the percent of population compared to world pop, and the countries' codes
countries = [x[0] for x in result]
percentPop = [x[1]/totalPop for x in result]
codes = [x[2] for x in result]
print(countries)
print(codes)

for x in percentPop:
    print(x)

#gets the count of all the major cities in the world
mycursor.execute("SELECT COUNT(*) FROM myworld.majorcity")
result = mycursor.fetchone()
majorCount = result[0]
print(majorCount)

#gets the count of major cities in the world for each country in the list
counts = []
for x in codes:
    query = "SELECT COUNT(id) FROM myworld.majorcity WHERE CountryCode ='" + x + "'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    counts.append(result[0])
print(counts)

#gets the percentage of major cities for each country in the list
percentCity = [x/majorCount for x in counts]
print(percentCity)

#visualizes all of the data gathered
fig, axes = plt.subplots(1, 2)

#creates bar graph
axes[0].bar(countries, percentPop, color = '#539caf', align = 'center')
axes[0].set_title("Percentage of world population of the top 10 populated countries")
axes[0].set_xlabel("Countries")
axes[0].set_ylabel("Percentage of World Population")

#creates pie graph
axes[1].pie(percentCity, labels = countries, autopct='%1.2f%%')
axes[1].set_title("Percent of major cities present in each country")

#shows the graphics
plt.show()

