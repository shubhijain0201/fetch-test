#To run the code, please use the command python codingtest.py <points>
#Please ensure the "transactions.csv" file is present in the same directory as the code.
#Please ensure the "transactions.csv" file contains valid data to get the expected output.

import pandas as pd
import json
import sys

sys.tracebacklimit = 0
transactionsData = pd.DataFrame()

def getPointsBalance(spendPoints):
	transactionsData.sort_values("timestamp", axis=0, ascending=True,inplace=True, na_position='first')

	for index, row in transactionsData.iterrows():
		if(spendPoints > row.points) :
			spendPoints = spendPoints - row.points
			transactionsData.at[index, 'points'] = 0
		else:
			transactionsData.at[index, 'points']  = transactionsData.at[index, 'points'] - spendPoints
			break
	pointBalancesData = transactionsData.groupby(['payer'])['points'].sum()

	finalJsonData = pointBalancesData.to_dict()
	jsonObject = json.dumps(finalJsonData, indent = 4) 
	print(jsonObject)      	

def main():

	try:
	        transactionsData = pd.read_csv("transactions.csv");
	except pd.errors.EmptyDataError as emptyDataError:
		print(emptyDataError.args)
		print("The csv file does not contain any data to be read. Please use another file with valid data")
		sys.exit(1)
	except FileNotFoundError:
        	print("The csv file does not exist in the working directory. Please use a valid file with the filename \"transactions.csv\" present in the current working directory.")
        	sys.exit(1)

	points = int(sys.argv[1])
	if(points < 0):
		raise ValueError("Cannot spend negative amount of points. The points to be spent by the user must be positive or 0")
		sys.exit(1)
	getPointsBalance(points)

main()
