import logging
import sys
import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests

serverIP = 'localhost'
serverPort = 12345
1
def runGame():
    maxSkillPool = 300
    losersSkillTotal = 0
    totalPlayersSkill = 0
    randomPlayer = requests.get(
        'https://lxe6tkenk6.execute-api.us-east-1.amazonaws.com/default/getRandomPlayer'
    )
    
    print("Requesting Game")
    print("Requesting Random Player from Database: ")
    randomPlayer = randomPlayer.json()
    print(randomPlayer)
    logging.info("Random Player: "+randomPlayer['playerID']+"entering Match at "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((serverIP,serverPort))
        sock.sendall(bytes(json.dumps(randomPlayer['playerID']), 'utf8'))
        data = sock.recv(1024)

    # Get Opponents from Match Making Server
    playersFromServer = json.loads(data)
    allPlayersInGame = []
    allPlayersInGame.append(randomPlayer)
    totalPlayersSkill += randomPlayer['skill']
    print("Players entering from server: ")
    for player in playersFromServer:
        print(player)
        allPlayersInGame.append(player)
        totalPlayersSkill += player['skill']
        logging.info("Players: "+player['playerID']+"entering Match at "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))

    winner = random.choice(allPlayersInGame)
    winner['wins'] += 1
    logging.info("Player "+winner['playerID']+"has won the Match at "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    for loser in allPlayersInGame:
        if loser != winner:
            losersSkillTotal += loser['skill']
    
    winner['skill'] += (losersSkillTotal/totalPlayersSkill) * maxSkillPool
    print("Points earned: "+str((losersSkillTotal/totalPlayersSkill) * maxSkillPool))
    print("Winner is: ")
    print(winner)
    
    



def main():
    print("Running client")
    simulationRuns = input("Game(s) to Simulate on Matchmaking Server: ")
    count = 0;
    while count < int(simulationRuns):
        print('Game ID: ' + str(count))
        logging.info("Game "+str(count+1)+" requested at time "+datetime.now().strftime("%d.%b %Y %H:%M:%S"))
        runGame()
        count += 1


if __name__ == '__main__':
    logging.basicConfig(filename='clientSim.log', level=logging.INFO)
    logging.info("Running Client on Host at: "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    main()