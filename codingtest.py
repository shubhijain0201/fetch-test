#To run the code, please use the command python codingtest.py <points> OR python3 codingtest.py <points> where "points" is a required input. 
#Please ensure the "transactions.csv" file is present in the same directory as the code.
#Please ensure the "transactions.csv" file contains valid data to get the expected output.

import json
import pandas as pd
import sys

sys.tracebacklimit = 0
transactionsData = pd.DataFrame()

def getPointsBalance(spendPoints):
	try:
		transactionsData.sort_values("timestamp", axis=0, ascending=True,inplace=True, na_position='first')
	except KeyError as keyError:
		print(keyError.args)
		print("Timestamp column is not present in the csv file. Please ensure the csv file contains valid data")
		sys.exit(1)

	for index, row in transactionsData.iterrows():
		if(spendPoints > row.points) :
			#If the user wants to spend more points than the payer, then the payer lets them use all the points the payer has for them.
			spendPoints = spendPoints - row.points
			transactionsData.at[index, 'points'] = 0
		else:
			transactionsData.at[index, 'points']  = transactionsData.at[index, 'points'] - spendPoints
			break

	#After the payers have given the points to the user, we want to find the balance points for each payer
	pointBalancesData = transactionsData.groupby(['payer'])['points'].sum()

	finalJsonData = pointBalancesData.to_dict()
	jsonObject = json.dumps(finalJsonData, indent = 4) 
	print(jsonObject)      	

def main():

        #Checking that all input is valid.
        try:
                global transactionsData
                transactionsData = pd.read_csv("transactions.csv")
        except pd.errors.EmptyDataError as emptyDataError:
                print(emptyDataError.args)
                print("The csv file does not contain any data to be read. Please use another file with valid data")
                sys.exit(1)
        except FileNotFoundError as fileNotFoundError:
                print(fileNotFoundError.args)
                print("The csv file does not exist in the working directory. Please use a valid file with the filename \"transactions.csv\" present in the current working directory.")
                sys.exit(1)

        points = 0
        try:
                points = int(sys.argv[1])
        except IndexError as indexError:
                print(indexError.args)
                print("Input value for points has not been provided. Please provide a non-negative value of points which the customer can spend")
                sys.exit(1)
        if(points < 0):
                raise ValueError("Cannot spend negative amount of points. The points to be spent by the user must be positive or 0")
                sys.exit(1)

        getPointsBalance(points)

main()
