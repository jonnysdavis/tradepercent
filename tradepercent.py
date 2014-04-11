#!/usr/bin/env python
import time
import ystockquote
global up
global dwn
global stocks

dwn = 0
up = 0
stocks = 0
assets = 0
count = 0


def main():
	print '--------------------------------------'
	#Starting values
	dwn = float(raw_input('The stocks should be sold when they LOSE what percent?\n>>'))
	up = float(raw_input('The stocks should be sold when they GAIN what percent?\n>>'))
	dwn = 1 - dwn/100
	up = 1 + up/100
	count = 0
	stillown = True
	stocks,initworth = stockInit(up,dwn)
	print 'Starting Worth: ' + str(initworth) + '\n--------------------------------------'
	change = False
	#Convert sell values to decimals ready for multiplying
	while(stillown==True):
		stocks = updatePrices(stocks)
		stocks = checkSell(stocks,count)
		print 'CHECKED'
		stillown = checkEnd(stocks,initworth)
		count+=1
		
def checkSell(stocks3,counter):
	filne = "stocks.txt"
	f = open(filne, 'r+')
	lines = f.readlines()
	for i in range(1, len(lines)):
		place = i-1
		if(((float(stocks3[4][place])<=float(stocks3[7][place]))or(float(stocks3[4][place])>=float(stocks3[8][place])))and stocks3[5][place]==True):
			stocks3[5][place] = False
			stocks3[6][place] = stocks3[4][place]
			print str(stocks3[0][place]) + ' was just sold at ' + str(stocks3[6][place]) + ' and its starting price was ' + str(stocks3[2][place])
			action = True
	else:
		if(counter%15==0):
			print 'No action. Current Worth: ' + str(getWorth(stocks3))
				
	return stocks3
	
def stockInit(up2,dwn2):
	initworth=0
	#0=ticker,1=shares,2=start price, 3=price*shares , 4=current price, 5=still own,6=sell price,7 sell down, 8 sell up
	filne = "stocks.txt"
	f = open(filne, 'r+')
	lines = f.readlines()
	stocks = [[0 for y in xrange(len(lines)-1)] for x in xrange(len(lines)+10)]
	for i in range(1, len(lines)):
		place = i-1
		templn = lines[i]
		stocks[0][place],stocks[1][place] = templn.split()
		stocks[2][place] = ystockquote.get_price(stocks[0][place])
		stocks[3][place] = float(stocks[2][place])*float(stocks[1][place])
		stocks[4][place] = stocks[2][place]
		#Set all to own, and sell to 0
		stocks[5][place]=True
		stocks[6][place]=0
		#Add value to your initial worth
		initworth+=stocks[3][place]
		#Set sell down and sell up values
		stocks[7][place] = float(stocks[2][place]) * float(dwn2)
		stocks[8][place] = float(stocks[2][place]) * float(up2)
	return stocks,initworth

def updatePrices(stocks2):
	filne = "stocks.txt"
	f = open(filne, 'r+')
	lines = f.readlines()
	for i in range(1, len(lines)):
		place = i-1
		#Only update if stock is owned
		if(stocks2[5][place]==True):
			stocks2[4][place] = ystockquote.get_price(stocks2[0][place])
			
	return stocks2

def checkEnd(stocks2,start):
	stillown = False
	filne = "stocks.txt"
	f = open(filne, 'r+')
	lines = f.readlines()
	for i in range(1, len(lines)):
		place = i-1
		if(stocks2[5][place]==True):
			return True
	final = start - getWorth(stocks2)
	if(start>getWorth(stocks2)):
		print 'Done! You lost ' + str(final) + ', sorry about that.'
	else:
		print 'Done! You gained ' + str(final*-1) + ', hooray!'
	return False

def getWorth(stocks2):
	assets = 0
	filne = "stocks.txt"
	f = open(filne, 'r+')
	lines = f.readlines()
	for i in range(1, len(lines)):
		place = i-1
		if(stocks2[5][place]==True):
			assets+=float(stocks2[4][place])*float(stocks2[1][place])
		else:
			assets+=float(stocks2[6][place])*float(stocks2[1][place])
	return assets
	
if __name__ == '__main__':
	main()
