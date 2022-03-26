import requests
import matplotlib.pyplot as plt
import numpy as np

swgohUrl = "http://swgoh.gg"

def fetchGuild(guildId):
    function = "/api/guild-profile/" + guildId
    
    response = requests.get(swgohUrl + function)
    guildInfo = response.json()
    
    return guildInfo
    
def parseGuildInfo(data):
    guildAllyCodes = {}
    
    for key in data['data']['members']:
        allyCode = key['ally_code']

        guildAllyCodes[allyCode] = {}
        guildAllyCodes[allyCode]['name'] = key['player_name']
        guildAllyCodes[allyCode]['total_power'] = key['galactic_power']

    return guildAllyCodes
    
def fetchPlayerInfo(allyCode):
    function = '/api/player/' + str(allyCode)
    
    response = requests.get(swgohUrl + function)
    playerInfo = response.json()
    
    return playerInfo
    
def parsePlayerInfo(playerInfo):
    playerNiceInfo = {}
    playerNiceInfo['name'] = playerInfo['data']['name']
    playerNiceInfo['character_power'] = playerInfo['data']['character_galactic_power']

    return playerNiceInfo
    
def fetchAllyModInfo(allyCode):
    function = '/api/player/' + str(allyCode) + '/mods/'
    
    response = requests.get(swgohUrl + function)
    allyModInfo = response.json()
    
    return allyModInfo
    
def parseModInfo(modInfo):
    speedData = {}
    sixDot = 0

    for key in modInfo['mods']:
        primary = key['primary_stat']
        slot = key['slot']
        rarity = key['rarity']

        if rarity >= 6:
            sixDot = sixDot + 1
        
        if("Speed" not in primary['name']):
            secondary = key['secondary_stats']
            
            foundSpeed = False
            for second in secondary:
                if("Speed" in second['name']):
                    foundSpeed = True
                    speed = second['display_value']
                                        
                    if(speed not in speedData):
                        speedData[speed] = {}
                        speedData[speed]['count'] = 0
                        speedData[speed]['rarity'] = {}
                        speedData[speed]['slot'] = {}
                        
                    speedData[speed]['count'] = speedData[speed]['count'] + 1
                        
                    if(slot not in speedData[speed]['slot']):
                        speedData[speed]['slot'][slot] = 0
                    speedData[speed]['slot'][slot] = speedData[speed]['slot'][slot] + 1
                    
                    if(rarity not in speedData[speed]['rarity']):
                        speedData[speed]['rarity'][rarity] = 0
                    speedData[speed]['rarity'][rarity] = speedData[speed]['rarity'][rarity] + 1
                    
            if(not foundSpeed):
                speed = 0
                if(speed not in speedData):
                    speedData[speed] = {}
                    speedData[speed]['count'] = 0
                    speedData[speed]['rarity'] = {}
                    speedData[speed]['slot'] = {}
                    
                speedData[speed]['count'] = speedData[speed]['count'] + 1    
                
                if(slot not in speedData[speed]['slot']):
                    speedData[speed]['slot'][slot] = 0
                speedData[speed]['slot'][slot] = speedData[speed]['slot'][slot] + 1
                
                if(rarity not in speedData[speed]['rarity']):
                    speedData[speed]['rarity'][rarity] = 0
                speedData[speed]['rarity'][rarity] = speedData[speed]['rarity'][rarity] + 1
        
    return (sixDot, speedData)

def calculateThrakenScore(playerData, speedData, sixDot):
    modScore = sixDot
        
    for speed in speedData:
        speedVal = float(speed)
        
        if(speedVal >= 15 and speedVal < 20):
            modScore += (speedData[speed]['count'])
        elif(speedVal >= 20 and speedVal < 25):
            modScore += (3.0 * speedData[speed]['count'])
        elif(speedVal >= 25):
            modScore += (9.0 * speedData[speed]['count'])
            
    thrakenScore = (modScore / playerData['character_power'] * 100000)
    return thrakenScore

def calculateDSRScore(playerData, speedData):
    modScore = 0.0
    
    for speed in speedData:
        speedVal = float(speed)
    
        if(speedVal >= 15):
            modScore += (speedData[speed]['count'])
            
    dsr = (modScore / playerData['character_power'] * 100000)
    return dsr

def createModPlot(speedData):
    fiveDot = np.zeros(31)
    sixDot = np.zeros(31)
    labels = np.arange(31)
    
    print(labels)
    
    for speed in speedData:
        speedVal = int(speed)
        
        print(speedData[speed])
        
        if 5 in speedData[speed]['rarity']:
            fiveDot[speedVal] = int(speedData[speed]['rarity'][5])
            
        if 6 in speedData[speed]['rarity']:
            sixDot[speedVal] = int(speedData[speed]['rarity'][6])
        
    plt.bar(labels, fiveDot)
    plt.bar(labels, sixDot)
    plt.show()

def main():
    guildId = "9xQSut4_TdOD3pDfwbAbXA/"
    guildInfoJson = fetchGuild(guildId)
    allyCodes = parseGuildInfo(guildInfoJson)
    
    for ally in allyCodes:        
        playerInfo = fetchPlayerInfo(ally)
        playerInfoNice = parsePlayerInfo(playerInfo)
       
        if playerInfoNice['name'] == "Vincent":
            modInfo = fetchAllyModInfo(ally)
            (sixDot, speedInfo) = parseModInfo(modInfo)
            
            thrakenScore = calculateThrakenScore(playerInfoNice, speedInfo, sixDot)
            dsrScore = calculateDSRScore(playerInfoNice, speedInfo)
            
            print(playerInfoNice['name'], thrakenScore, dsrScore)
            
            createModPlot(speedInfo)
            
            exit(-1)
            
main()