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
  exemail = ['example@email.com', 'example@email.com', '@mydomain.com']
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
  except:
    logger.error(f"Event emails not found")

  #remove duplicates
  emails = set(emails)
  #remove excluded emails and domains
  logger.debug(f"Emails after remove duplicates: {emails}")
  checkemails = emails.copy()
  for email in checkemails:
    logger.debug(f"Inspecting: {email}")
    for exclude in exemail:
      logger.debug(f"Comparing: {exclude} to {email}")
      if str(exclude) in str(email):
        logger.debug(f"Removing excluded email: {email}")
        try:
          emails.remove(email)
        except:
          logger.error(f"Could not remove email {email}")
        else:
          logger.debug(f"Removed {email} from list due to exclusion")
          break
  logger.debug(f"Event emails found: {str(emails)}")

  try:
    con = pymysql.connect(
      host="xx",
      user="xx",
      password="xx",
      database="xx",
      port=3306,
      connect_timeout=15
    )
    logger.debug(f"Connection: {con}")
    cur = con.cursor()
  except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

  for email in emails:
    try:
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
      logger.error(f"Unable to perform lookup in database for {email}")

  for addemail in addemails:
    try:
      logger.info(f'Adding to email {addemail} to database')
      addquery='INSERT INTO email_blacklist (email, blocked) VALUES (%s, 1);'
      cur.execute(addquery, addemail)
      con.commit()
    except:
      logger.error(f"Failed to add {addemail} to blacklist")
    else:
      logger.info(f"Successfully added {addemail} to blacklist")

  try:
    con.close()
  except:
    logger.error(f"Error closing connection to database")
  else:
    logger.debug(f"Closed database connection")
