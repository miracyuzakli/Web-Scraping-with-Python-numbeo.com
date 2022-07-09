
# For web scraping
import requests 
from bs4 import BeautifulSoup
import pandas as pd

# To print colored text in terminal
import colorama
from colorama import Fore, Back, Style
colorama.init()


class webScraping:

    def __init__(self) -> None:
        self.DataDict = dict()
        self.DataDict["CountryName"] = list()


    def getCountyNameList(self, countryURL = "https://www.numbeo.com/cost-of-living/"):

        res = requests.get(countryURL).text
        soup = BeautifulSoup(res, "html.parser")
        
        countyrlist = list()
        
        for a in  soup.find_all('a',href = True):
            if 'country_result' in a['href']:
                countyrlist.append(a["href"].split("=")[1])
            
        return countyrlist

    def getCountriesCostOfLiving(self, countryURL, countryName):

        self.DataDict["CountryName"].append(countryName)
        res = requests.get(countryURL).text
        soup = BeautifulSoup(res, "html.parser")
        table = soup.find("table", class_ = "data_wide_table")
        for row in table.find_all("tr"):
            column = row.find_all("td")
            if column != []:
                name = column[0].text.strip()
                price = column[1].text.strip()
                
                if name not in [i for i in self.DataDict.keys()]:
                    self.DataDict[name] = list()
                    self.DataDict[name].append(price)

                else:
                    self.DataDict[name].append(price)



    def CountryNameOperation(self, countryName): 

        countryName = countryName.replace("%28", "(")
        countryName = countryName.replace("%29", ")")
        countryName = countryName.replace("+", " ")
        
        return countryName

    def dataMerge(self):
        
        countyrsList = self.getCountyNameList()
        print(Fore.LIGHTRED_EX, "Country names successfully imported (total number of countries : {})\n".format(len(countyrsList)))
        counter = 1
        for countryName in countyrsList:
            countryName_ = self.CountryNameOperation(countryName)
            url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country={}&displayCurrency=USD".format(countryName)
            self.getCountriesCostOfLiving(url, countryName_)
            print(Fore.GREEN, "    Successfully completed ", Fore.MAGENTA, "--------------------- ",
                Fore.WHITE, "{}/{}".format(counter, len(countyrsList)), Fore.MAGENTA, "----", Fore.BLUE, "{}".format(countryName_))

            counter += 1

        return self.DataDict

    def getDataFrame(self):
        dataDict = self.DataDict
        counterDict = dict()
        
        for i in dataDict:
            if str(len(dataDict[i])) not in [ky for ky in counterDict.keys()]:
                
                counterDict[str(len(dataDict[i]))] = 1
            else:
                counterDict[str(len(dataDict[i]))] += 1
                
        maxValue = max(counterDict, key = counterDict.get)
        
        lastDict = dict()
        for i in dataDict:
            if len(dataDict[i]) == int(maxValue):
                lastDict[i] = dataDict[i]
                
        print(Fore.LIGHTGREEN_EX, "\nTransactions completed successfully.", Fore.RESET)
        
        return pd.DataFrame(lastDict)
            
            
                
            

WS = webScraping()

WS.dataMerge()

data = WS.getDataFrame()
print(data)

























