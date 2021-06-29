import mysql.connector
import urllib.request
import re

print ("we will try to open this url, in order to get IP Address")

url = "http://checkip.dyndns.org"

print (url)

request = urllib.request.urlopen(url).read()

print ("your IP Address is: ",  str(request))

mydb = mysql.connector.connect(
  host="xx",
  user="xx",
  password="xx",
  database="xx",
  connection_timeout=15
)

print(mydb)