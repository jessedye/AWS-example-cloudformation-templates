import boto3
import json
import re
import logging
import os
import sys
import pymysql

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# main function
def handler(event, context):

  emails = []
  addemails = []
  #excluded email
  exemail = ['exclude1@email.com', 'exclude2@email.com']
  try:
    event = str(event)
    logger.debug(f"Event: {event}")
    eventemails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", event)
    if eventemails:
      for eventemail in eventemails:
        logger.debug(f"Event Email: {eventemail}")
        eventemail = str(eventemail)
        eventemail = eventemail.replace("['", "")
        eventemail = eventemail.replace("']", "")
        logger.debug(f"Event Formatted Email: {eventemail}")
        emails.append(eventemail)

      #remove duplicates
      emails = list(dict.fromkeys(emails))
      for exclude in exemail:
        if exclude in emails:
          logger.debug(f"Removing excluded email: {exclude}")
          emails.remove(exclude)
        
      logger.debug(f"Event emails found: {str(emails)}")

  except:
    logger.error(f"Event emails not found")

  try:
    con = pymysql.connect(
      host="xxxx",
      user="xxx", 
      password="XXXXXX",
      database="xxx",
      port=3306,
      connect_timeout=30
    )
    logger.debug(f"Connection: {con}")
    cur = con.cursor()
  except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

  try:
    for email in emails:
      logger.debug(f"Checking if email: {email} already exists in blacklist...")
      selquery='SELECT * FROM email_blacklist WHERE email=%s;'
      cur.execute(selquery, email)
      checkrow = cur.fetchone()
      if checkrow == None:
        logger.info(f"{email} not found, adding")
        addemails.append(email)
      else:
        logger.info(f"{email} already exists, skipping!")
  except:
    logger.error(f"Unable to do lookup on database..")

  try:
    for addemail in addemails:
      logger.debug(f'Adding to email {addemail} to database')
      addquery='INSERT INTO email_blacklist (email, blocked) VALUES (%s, 1);'
      cur.execute(addquery, addemail)
      con.commit()
  except:
    logger.error(f"Unable to add record to database")

  try:
    con.close()
  except:
    logger.error(f"Error closing connection to database")  