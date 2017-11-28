from __future__ import print_function
import datetime
import time
import json
import os
import xml.etree.ElementTree as ET
import requests
import sys

def loadXML(XMLpath):
    # Load configuration from XML

    tree = ET.parse(XMLpath)
    root = tree.getroot()

    xmlLife = int(root.findall('XMLlife')[0].text)*60

    outFolder = root.findall('outfolder')[0].text

    timeStep = int(root.findall('timeStep')[0].text)

    selectCurrency = []
    currency = root.findall('selectCurrency')
    for c in currency:
        for node in c.getiterator():
            if node.tag =='item':
                selectCurrency.append(node.text)

    return xmlLife,outFolder,timeStep,selectCurrency

if __name__ == '__main__':

    # Load XML from file
    XMLpath = sys.argv[1]#'./conf.xml'
    lastXML = datetime.datetime.now()
    xmlLife, outFolder, timeStep, selectCurrency = loadXML(XMLpath)

    # Base API URL
    baseURL = 'https://api.coinmarketcap.com/v1/ticker/'

    # Create output folder if not exists
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    # Structure with last update time
    lastupdate = dict()

    print ('Initialization Completed...')

    # Core Loop
    while 1:

        # Processing Loop
        try:
            timeStamp = datetime.datetime.now()
            print (timeStamp.strftime('%Y%m%d_%H%M%S') + ': iteration started...')

            # If XML lifetime is expired load configuration
            if (timeStamp - lastXML).seconds > xmlLife:
                xmlLife, outFolder, timeStep, selectCurrency = loadXML(XMLpath)
                lastXML = datetime.datetime.now()
                print ('XML correctly updated...')

            # Evaluate name of output file according to actual date
            Fname = timeStamp.strftime('%Y%m%d')
            pathM = outFolder + Fname + '_liveMarketCap.json'
            errorPath = outFolder + Fname + '_liveMarketCapError.json'

            # Branch 1 - if XML contains string 'allcurrencies' download all currency information available
            if 'allcurrencies' in selectCurrency:
                message = requests.get(baseURL).json()

                for c in message:
                    currency = c['id']
                    print(currency, end='')

                    # Given a certain currency, if lastupdate time is known
                    # check if its value needs to be updated
                    if currency in lastupdate:
                        if int(c['last_updated']) > lastupdate[currency]:
                            lastupdate[currency] = int(c['last_updated'])
                            print(': updated value')
                            with open(pathM, "a") as myfile:
                                myfile.write(json.dumps(c))
                                myfile.write('\n')
                        else:
                            print(': nothing new...')

                    # if the currency is new in the list of last updated it would be added to the list
                    # and it's value is written in the output file
                    else:
                        lastupdate[currency] = int(c['last_updated'])
                        print(': updated value')
                        with open(pathM, "a") as myfile:
                            myfile.write(json.dumps(message))
                            myfile.write('\n')

            # Branch 2 - XML contains a list of currency
            else:

                for currency in selectCurrency:
                    try:
                        print(currency,end='')
                        message = requests.get(baseURL+currency).json()[0]
                        currencyID = message['id']

                        # Given a certain currency, if lastupdate time is known
                        # check if its value needs to be updated
                        if currencyID in lastupdate:
                            if int(message['last_updated']) > lastupdate[currencyID]:
                                lastupdate[currencyID] = int(message['last_updated'])

                                print (': updated value')
                                with open(pathM, "a") as myfile:
                                    myfile.write(json.dumps(message))
                                    myfile.write('\n')
                            else:
                                print (': nothing new...')

                        # if the currency is new in the list of last updated it would be added to the list
                        # and it's value is written in the output file
                        else:
                            lastupdate[currencyID] = int(message['last_updated'])
                            print(': updated value')
                            with open(pathM, "a") as myfile:
                                myfile.write(json.dumps(message))
                                myfile.write('\n')

                    #
                    except Exception as e:
                        print(': error')
                        with open(errorPath, "a") as errfile:
                            errfile.write(timeStamp.strftime('%Y%m%d_%H%M%S'))
                            errfile.write('  -  ')
                            errfile.write(str(e))
                            errfile.write('\n')

            print ('Iteration Ended')
            time.sleep(timeStep)

        # Error Management
        except Exception as e:
            with open(errorPath, "a") as errfile:
                errfile.write(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                errfile.write('  -  ')
                errfile.write(str(e))
                errfile.write('\n')
                time.sleep(timeStep/30)