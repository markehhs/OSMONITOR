import requests
import json
import datetime
import discord
import os
import time
from dotenv import load_dotenv

##
##

try:    
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    ETHAPIKEY = os.getenv('ETH_GAS_KEY')
except Exception as e:
    print("Setup error. Make sure your .env file is setup correctly. Checkout the readme for more help.\n" + e)

addrList = []
client = discord.Client()

def monitor(addr, delayTime):
    ## first grab the epoch time based on the delay time
    try:
        if delayTime < 0:
            print("Error, delay time must be greater than 0.")
            raise Exception(e)
        current_time = datetime.datetime.now()  # use datetime.datetime.utcnow() for UTC time
        oldTime = current_time - datetime.timedelta(minutes=delayTime)
        oldTimeEpoch = str(int(oldTime.timestamp() * 1000))  # in miliseconds
        ##now that we have the time lets go ahead and send the request
        ##when a transaction is made display the transaction
        url = "https://api.opensea.io/api/v1/events?account_address=" + addr + "&event_type=successful&only_opensea=false&offset=0&limit=20&occurred_after=" + oldTimeEpoch
        print(url)
        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)

        json_object = json.loads(response.text)

        json_formatted_str = json.dumps(json_object, indent=2)
        ##we now have the response so lets show the results
        newTransactionsCount = len(json_object['asset_events'])
        print("COUNT: " + str(newTransactionsCount) + " made since: " + str(delayTime) + " minutes ago.")
        c = 0
        for x in json_object['asset_events']:
            assetName = json_object['asset_events'][c]['asset']['name']
            assetImage = json_object['asset_events'][c]['asset']['image_url']
            assetDescription = json_object['asset_events'][c]['asset']['description']
            if assetDescription == None:
                assetDescription = "No description available."
            print("Asset name: " + assetName)
            print("Description\n" + assetDescription + "\n\n")
            print(assetImage)
            c += 1
        print(str(oldTimeEpoch))
    except Exception(e):
        ##need to add exception error handling here
        print("Error")
        print(e.with_traceback)

def monitor(addr):
    ## first grab the epoch time based on the delay time
    delayTime = 3600
    try:
        if delayTime < 0:
            print("Error, delay time must be greater than 0.")
            raise Exception(e)
        current_time = datetime.datetime.now()  # use datetime.datetime.utcnow() for UTC time
        oldTime = current_time - datetime.timedelta(minutes=delayTime)
        oldTimeEpoch = str(int(oldTime.timestamp() * 1000))  # in miliseconds
        ##now that we have the time lets go ahead and send the request
        ##when a transaction is made display the transaction
        url = "https://api.opensea.io/api/v1/events?account_address=" + addr + "&event_type=successful&only_opensea=false&offset=0&limit=20&occurred_after=" + oldTimeEpoch
        print(url)
        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)
        if response.ok:
            json_object = json.loads(response.text)

            json_formatted_str = json.dumps(json_object, indent=2)
            ##we now have the response so lets show the results
            newTransactionsCount = len(json_object['asset_events'])
            if newTransactionsCount >= 1:
                print("COUNT: " + str(newTransactionsCount) + " made since: " + str(delayTime) + " minutes ago.")
            c = 0
            for x in json_object['asset_events']:
                assetName = json_object['asset_events'][c]['asset']['name']
                assetImage = json_object['asset_events'][c]['asset']['image_url']
                assetDescription = json_object['asset_events'][c]['asset']['description']
                if assetDescription == None:
                    assetDescription = "No description available."
                print("Asset name: " + assetName)
                print("Description\n" + assetDescription + "\n\n")
                print(assetImage)
                c += 1
            ##print(str(oldTimeEpoch))
        else:
            print("OS is down.")
    except:
        print("Something went wrong.")
        
    


##f = open("json_response.txt", "w")
##f.write(json_formatted_str)
##f.close()

def add(addr):
    ##given an addr add to the list
    addrList.append(str(addr))


def main():
    ##thinking of a list of lists(addr:time) to hold all addresses to monitor
    ##this way we can just add or remove easily 
    #################################Discord setup
    @client.event
    async def on_message(message):
        ##check if the first character begins with !
        ##if it does split if by space
        if message.content[0] == "!":
            ##this is our command so now lets split by space and grab the word
            args = message.content.split(" ")
            ##now lets get the word after !
            command = args[0].split("!")[1]
            ##print(args[0])
            ##print(command)
            if command == "add":
                ##add addr function here
                if len(args) == 2:
                    ##good
                    add(args[1])
                    print("Added: " + str(args[1]) + " to the monitor.")
                    await message.channel.send("Added: " + str(args[1]) + " to the monitor.")
    cvar = 0
    while True:
        if cvar == 0:
            client.run(TOKEN)   
        print("Client.run done.")         
        for x in addrList:
            if x != None:
                print("Should be added.")
                monitor(x)
                time.sleep(5)
            else:
                print("No sales found.")
        cvar += 1
    
    

main()

