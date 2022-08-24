from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
from datetime import datetime, timedelta

#utilize twilio to send url link by text
def sendText(fightLink):
  #twilio account SID
  account_sid = 'XXXXXXXXXXXXXXXXXXXXXX'
  #twilio account auth token
  auth_token = 'XXXXXXXXXXXXXXXXXXXXXX'
  client = Client(account_sid, auth_token)

  message = client.messages \
    .create(
      #text message body containing the url link
      body=fightLink,
      #twilio phone number the text message is sent from
      from_='+15555555555',
      #personal phone number the text message is sent to
      to='+14444444444'
    )

#retrieves tomorrow's date, returns date formatted so it
#can be compared to the string on webpage Ex: "Aug 20"
def tomorrowDate():
  #tomorrow's date
  tomorrow = datetime.now() + timedelta(days=1) 
  tomorrow_formatted = tomorrow.strftime('%b %d')

  return tomorrow_formatted

#returns True if there is a fight tomorrow in Vegas
def fightTomorrowInVegas(fight):
  fightTomorrow = False
  fightVegas = False
  #tomorrow's date formatted to compare against date string from webpage
  tomorrow = tomorrowDate()
  #loops through all the strings in the div passed to function
  #these strings will contain fight date and location
  for string in fight.strings:
      if tomorrow == string:
        fightTomorrow = True
      if "Las Vegas" in string:
        fightVegas = True
  if fightTomorrow and fightVegas:
    return True
  else:
    return False

#driver function that checks if there is a fight in Vegas tomorrow
#and if there is, sends a notification text message containing fight link
def scrapeSite(soup):
  #list of divs on webpage containing schedule information for each fight
  fights = soup.find_all("div", class_="schedule-fight")
  #loop through each div
  for fight in fights:
    if fightTomorrowInVegas(fight):
      #finds link to the fight, passes link to the sendText function
      for link in fight.find_all('a'):
        fightLink = link.get('href')
        sendText(fightLink)  

def main():
  #url to be scraped, boxingscene.com's fight schedule page
  url = "https://www.boxingscene.com/schedule"

  #my user-agent
  headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

  #scrape the given url using Beautiful Soup
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  scrapeSite(soup)


if __name__ == "__main__":
  main()