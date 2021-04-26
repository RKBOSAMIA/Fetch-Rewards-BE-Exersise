# Fetch-Rewards-BE-Exersise

For this exercise, I have used the following technologies.

-> Python v3.8.0
-> flask  v1.1.1
-> Postman (to check endpoints)

I have provided the detailed working of the endpoints and functions in the source file in form of comments.

How to run the flask app?

-> Open Terminal/Command Prompt
-> Go to the Fetch Rewards directory
-> Enter command: python3 server.py

The above command starts the flask server on http://127.0.0.1:5000/

Steps to access endpoints:

1) I have used Postman. The post requests are in the form of [JSON] objects are made from [body]".
2) Endpoint (POST Request) : http://127.0.0.1:5000/addTransaction
  -> add [one] transaction at a time.
3) Endpoint (POST Request) : http://127.0.0.1:5000/spendPoints
  -> enter the number of points to spend in the form, {"points": val}
4) Endpoint (GET Request)  : http://127.0.0.1:5000/getBalance
  -> Returns the remaining points for each payer.
  

[THANK YOU]
