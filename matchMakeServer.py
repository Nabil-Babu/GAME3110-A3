import logging
import sys
import random
import socket
import time
from operator import itemgetter
from _thread import *
import threading
from datetime import datetime
import json
import requests

logging.basicConfig(filename='matchMakeServer.log', level=logging.INFO)

# Lambda Function API endpoints
allPlayersHTTPRequesrURL = 'https://2a8wbdelmg.execute-api.us-east-1.amazonaws.com/default/getAllPlayersFromDatabase'

def getPlayersForMatch(sock):
    while True:
        sock.listen()
        conn, addr = sock.accept()
        print("Player Requesting Match")
        with conn:
            playerIDRequest = conn.recv(1024)
            playerIDRequest = json.loads(playerIDRequest)
            if playerIDRequest != "":
                print("Player ID Requesting Match: "+playerIDRequest)
                logging.info("Player: "+playerIDRequest+" has requested a match at "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))
                response = requests.get(allPlayersHTTPRequesrURL)
                allPlayers = response.json()['Items']
                skillTolerance = 200
                challenger = None
                for player in allPlayers:
                    if player['playerID'] == playerIDRequest:
                        challenger = player
                print("The challenger is: ")
                print(challenger)
                skillTolerance += (0.50 * challenger['loss']) * 100
                print("Challanger Skill Tolerance: "+str(skillTolerance))
                # Potential Opponents
                opponentList = []
                for player in allPlayers:
                    if abs(player['skill']-challenger['skill']) <= skillTolerance and player != challenger:
                        opponentList.append(player)
                print("Players available to fight: ")
                for opponents in opponentList:
                    print(opponents)

                sortedOpponentList = sorted(opponentList, key=itemgetter('skill'))
                print("Sorted players available to fight: ")
                for sortedOpponents in sortedOpponentList:
                    print(sortedOpponents)

                while len(sortedOpponentList) > 2:
                    sortedOpponentList.pop();

                print("Trimmed sorted players available to fight: ")
                for trimsortedOpponents in sortedOpponentList:
                    print(trimsortedOpponents)
                    logging.info("Player: "+player['playerID']+" is entering the match at "+ datetime.now().strftime("%d.%b %Y %H:%M:%S"))

                response = json.dumps(sortedOpponentList)
                conn.sendall(bytes(response, 'utf8'))
            

serverIP = ''
serverPort = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((serverIP, serverPort))
    start_new_thread(getPlayersForMatch, (s,))
    while True:
        print("Boop")
        time.sleep(1)