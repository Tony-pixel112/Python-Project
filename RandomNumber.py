import random

from fontTools.merge import options

low=1
high = 100
options = ("rock", "paper", "scissors")
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10","A","Q","J","K"]

#number = random.randint(low, high)
#number = random.random()#gives you random number between 0 and 1
option = random.choice(options)
#random.shuffle(cards)#This shuffles the cards

print(cards)