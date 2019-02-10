import requests,json,time, telepot, sys
from pprint import pprint
import config


base_url = "https://unisport.fi/yol/api/v1/fi/reservables/{}?details=true&apiKey=drupal8test"

TOKEN = config.TOKEN
CHATID = config.CHATID

def checkAvaibility(code):
    url = base_url.format(code)
    try:
        req = requests.get(url)
        data = json.loads(req.content.decode("utf-8"))
        rootNode = data["items"][0]
        if rootNode["maxAttendees"] == rootNode["reservations"]:
            return False
        return True
    except Exception as err:
        print "Error: " + str(err)

def isCorrectClass(code):
    url = base_url.format(code)
    try:
        req = requests.get(url)
        data = json.loads(req.content.decode("utf-8"))
        if len(data) == 0:
            print "Class code " + code + " couldn't been found"
            exit(1)
        rootNode = data["items"][0]
        print "Start time: " + rootNode["startTime"]
        print "Venue " + rootNode["venue"]
        print "Class " + rootNode["activity"]
        user_input = raw_input("Is this correct (y/n) ")
        if user_input.lower() == "y":
            return rootNode
        print "Exiting..."
        return False
    except Exception as err:
        print "Error " + str(err)
        exit(1)

def main():
    if len(sys.argv) != 2:
        print "Please input class code!"
        exit(1)
    code = sys.argv[1]

    bot = telepot.Bot(TOKEN)
    #response = bot.getUpdates()
    #pprint(response)
    result = isCorrectClass(code)
    if not result:
        exit(0)

    previousAvaibility = False
    addedClass = "Lurkattavaksi: \n" \
    + result["activity"] + " " + result["startTime"] +"@" + result["venue"]
    bot.sendMessage(CHATID, addedClass)
    while True:
        avaibility = checkAvaibility(code)
        if avaibility and not previousAvaibility:
            bot.sendMessage(CHATID, "Booty vappaana!!")
        elif previousAvaibility and not avaibility:
            bot.sendMessage(CHATID, "Aaand it's gone")

        previousAvaibility = avaibility
        time.sleep(60)

if __name__== "__main__":
    main()

