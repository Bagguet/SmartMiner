from bs4 import BeautifulSoup
from utils import log
class SoupManagerCoin:
    def __init__(self,html,hashrate):
        self.myHashrate = hashrate
        self.rawHtml = html
        self.informations = {}
        self.soup = None
        self.UnitConversion = {"H":0.001,"K":1,"M":10**3,"G":10**6,"T":10**9,"P":10**12}
        self.minerTax = 0.01
        self.poolTax = 0
        self.getSoup()
        self.getCoinName()
        self.getNetworkHashrate()
        self.getPrice()
        self.getEmission()
        self.calculateIncomePerDay()
    
    def floatHandler(self,value):
        try:
            return float(value)
        except:
            print(f"error while converting {value}")
            return 0
    def getSoup(self):
        self.soup = BeautifulSoup(self.rawHtml,"lxml")
        return self.soup
    
    def getCoinName(self):
        self.symbol = ""
        try:
            coinName = self.soup.find("h1",class_="box-title").text.split()
            for i,string in enumerate(coinName):
                if string == "NEW":
                    self.symbol = coinName[i-1][1:-1] 
                    self.coinName = " ".join(coinName[0:i-1])
                    break
        except:
            self.coinName = self.soup.find("h1",class_="box-title").text.split()[0]
        self.informations["Coin name"] = self.coinName
        self.informations["Symbol"] = self.symbol
            
    def getNetworkHashrate(self):
        netHashrateText = self.soup.find(id="nethash").text.split()
        hashrateText = self.soup.find(id="poolshash").text.split()
        calc_netHashrate = float(netHashrateText[0])*float(self.UnitConversion[netHashrateText[1][0]])
        calc_hashrate = float(hashrateText[0])*float(self.UnitConversion[hashrateText[1][0]])
        
        if  calc_netHashrate < calc_hashrate:
            netHashrateText = hashrateText

        self.netHashrate = self.floatHandler(netHashrateText[0])
        self.netHashrateUnit = netHashrateText[1]
            
        self.informations["Net hashrate"]= self.netHashrate
        self.informations["Net hashrate unit"]= self.netHashrateUnit

    def getPrice(self):
        html = self.soup.find("div",class_="columnhome_right")
        self.price = float(html.find(id="stats_priceusd").find("b").text)
        self.informations["Price"] = self.price

    def getEmission(self):
        try:
            if self.coinName == "Etica":
                self.emission = 4602.24
            elif self.coinName == "Zephyr":
                self.emission = float(self.soup.find(id="stats_supply_emission").text.split()[0])*0.75
            else:
                self.emission = float(self.soup.find(id="stats_supply_emission").text.split()[0])
            self.informations["Emission"] = self.emission
        except:
                log(f'[WARN] {self.informations["Coin name"]} no emmision information')
                self.emission = 0
        
    def calculateIncomePerDay(self):
        if self.emission == 0:
            self.informations["Income per day"] = 0
            self.informations["Income per day in usd"] = 0
            return
        convertedNetHashrate = self.UnitConversion[self.netHashrateUnit[0]]*self.netHashrate
        try:
            self.totalTax = 1-(self.poolTax + self.minerTax)
            self.incomePerDay = self.myHashrate/convertedNetHashrate*self.emission*self.totalTax
        except:
            self.incomePerDay = 0 
            log(f"[Error] {self.coinName} income calculation")
        
        self.incomePerDayInUsd = self.incomePerDay*self.price
        self.informations["Price"] = self.price
        self.informations["Income per day"] = self.incomePerDay
        self.informations["Income per day in usd"] = self.incomePerDayInUsd
    def getInformation(self):
        return self.informations
