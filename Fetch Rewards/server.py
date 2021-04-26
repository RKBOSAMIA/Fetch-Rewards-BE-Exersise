from flask import Flask,request,jsonify
import collections

app = Flask(__name__)

"""
Below are some global variables for the application.
transactions = a list that stores all the transactions.
totalPoints = a dictionary that stores the total points for each payer.
availablePoints = a variable that stores the total available points in the system.
payerPointsDeducted = a dictionary that keeps track of how many points each payer has paid, on each spendPoints() call

"""
transactions = []
totalPoints = collections.defaultdict(int)
availablePoints = 0
payerPointsDeducted = collections.defaultdict(int)

"""
Endpoint: http://127.0.0.1:5000/addTransaction
Description: accepts POST request in body to add the transactions.
Returns: A Success/Failure message
"""

@app.route('/addTransaction',methods=['POST'])
def addTransaction():
    global transactions
    global availablePoints
    global totalPoints

    try:
        transaction = request.get_json()
        totalPoints[transaction['payer']] += transaction['points']
        availablePoints += transaction['points']
        transactions.append(transaction)

        return 'Transaction added successfully !!'
    except:
        return 'Error occured while adding the transaction !!'

"""
Endpoint: http://127.0.0.1:5000/spendPoints
Description: 
1) Accepts POST request in body to spend certain number of points.
2) Spends points according to the rules mentioned in the exercise.
3) Updates all global variables accordingly.
Returns:
1) Error message if total available points in the system is less than the request for points to spend
2) A list of JSON objects containing the number of points deducted for each payer.

"""
@app.route('/spendPoints',methods=['POST'])
def spendPoints():

    try:
        # sort the transactions on the basis of timestamp to get the oldest transaction first
        transactions.sort(key = lambda x:x['timestamp'])
        pointsToSpend = request.get_json()
        pointsToSpend = pointsToSpend['points']
        
        global availablePoints
        global payerPointsDeducted

        # if the availablePoints in the system is less than the pointsToSpend, return error.
        if availablePoints < pointsToSpend:
            return 'Error: Not enough points available !!'

        # reset payerPointsDeducted on each call, to store only the current transaction details.
        payerPointsDeducted = collections.defaultdict(int)

        # loop through each transaction, update the points to zero if a transaction is used completely
        for transaction in transactions:
            if transaction['points']:
                payer = transaction['payer']
                currPoint = transaction['points']

                # if pointsToSpend is not 0, continue with the loop else break
                if pointsToSpend:
                    # if payer points are less than the pointsToSpend, use up all points in the transaction
                    if currPoint <= pointsToSpend:
                        # condition to ensure payer's point doesn't go negative
                        if totalPoints[payer] - currPoint >= 0:
                            pointsToSpend -= currPoint
                            payerPointsDeducted[payer] += -currPoint
                            transaction['points'] = 0
                    # else take all the remaining pointsToSpend from the transaction have points more than the pointsToSpend
                    elif currPoint > pointsToSpend:
                        payerPointsDeducted[payer] = -pointsToSpend
                        transaction['points'] -= pointsToSpend
                        pointsToSpend = 0
                else:
                    break
        
        # update total points for each user as well as the total available points in the system.
        for payer,points in totalPoints.items():
            totalPoints[payer] += payerPointsDeducted[payer]
            availablePoints += payerPointsDeducted[payer]

        returnValue = []

        # set the return value in the desired format
        for payer,points in payerPointsDeducted.items():
            returnValue.append({'payer':payer,'points':points})

        return jsonify(returnValue)
    except:
        return 'Error occurred while processing the points !!'

"""
Endpoint: http://127.0.0.1:5000/getBalance
Description: accepts GET request to get the remaining balance for each payer.
Returns: A list of JSON objects containing the remaining balance for each payer.

"""
@app.route('/getBalance',methods = ['GET'])
def getBalance():
    return jsonify({"Remaining Balance":totalPoints})

if __name__ == '__main__':
    app.run()