from dotenv import load_dotenv
import json
import os
import requests
import pandas as pnd 
from datetime import datetime
import datetime

load_dotenv() 

apikey = str(os.environ.get("ALPHAVANTAGE_API_KEY"))
#Shoutout to @Chenmi1997 for the help here on the "str(...)" part"

#intro Messages
print("--------------------------------------------------- ")
print(" ")
print("WELCOME TO THE BLUECHIP STOCK PICKER ")
print(" ")
print("This application helps volatility traders choose stocks that have low volatility")
print("in order to assist in decisionmaking with regards to determining which equities") 
print("to write calls and puts for.")
print(" ")

print("Disclaimer: this is not professional investment advice")
print(" ")

print("--------------------------------------------------- ")

print(" ")

#requesting ticker for the stock
while True:
    ticker = input("Please enter the ticker of your stock of choice: ") 
    #Shoutout to @hiepnguyen for helping me realize a while loop is optimal for this
    
    if ticker.isdigit():
        print("Invalid entry: a stock ticker only uses characters - integers or symbols are not permitted")
    else:
        pull = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=" + apikey)
        
        if "Error" in pull.text:
            print("Error: stock either cannot be found or is not listed on Alpha Vantage - please enter another stock ticker")
        else:
            break  

j=pull.json()

#variables created for the date to be used later
time = datetime.datetime.now()
a = time.strftime("%Y")
b = time.strftime("%m")
c = time.strftime("%d")    
d = time.strftime("%I")
e = time.strftime("%M")
f = time.strftime("%p")

t,opn,h,l,close,vol = [],[],[],[],[],[]


#adds values pulled from Alpha Vantage
for lx, value in j["Time Series (Daily)"].items():
    t.append(lx)
    
    opn.append(float(value["1. open"]))

    h.append(float(value["2. high"]))
    
    l.append(float(value["3. low"]))
    
    close.append(float(value["4. close"]))
    
    vol.append(float(value["5. volume"]))
#Shoutout to THE @Chenmi1997
#interestingly enough, before I used "(float(...))", the data was coming out wrong
#for companies where the prices fluctuated between 4 digits and 5, the 4 digit numbers were not being read somehow

print(" ")
print("--------------------------------------------------- ")
print(" ")
print("Stock Ticker: " + ticker)
print(" ")
print("Program Run On: " + a + "-" + b + "-" + c + " " + d + ":" + e + " " + f)
print(" ")
print("...")
print(" ")
print("Now saving the requested information")
print(" ")
print("...")
print(" ")

#data headers are formatted in order to be put into a CSV
output = pnd.DataFrame(
    {
        "Time":t, "Open":opn, "High": h, "Low":l, "Close":close, "Volume": vol,
    }
)


#deletes a file if it is named in the same way (the data would essentially be the same)
while True:
    if os.path.isfile("data/" +ticker + "_" + a + b  + c + ".csv"):
        os.remove("data/" + ticker + "_" + a + b  + c + ".csv")
        #shoutout to this link https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists
    else:
        break

#data is pushed into a CSV file
output.to_csv("data/" + ticker + "_" + a + b  + c + ".csv")

print("File saved as " + ticker + "_" + a + b  + c + ".csv in the 'data' folder")
print(" ")
print("--------------------------------------------------- ")
print(" ")
print(" ")
print("CALCULATING BASIC RELEVANT DATA")
print(" ")
print("...")
print(" ")
print("LAST DAY OF AVAILABLE DATA: " + output.iloc[0]["Time"])
print("")

def dolval(valueinput):
    return "{0:,.2f}".format(valueinput)
#Shoutout Professor Rossetti for the formatting here @s2t2

#calculates the closing, high, and low prices
recclose = (float(output.iloc[0]["Close"]))
reclow = (float(min((output["Low"]))))
rechigh = (float(max((output["High"]))))

#redundant series of code that I ended up not removing, but initially had caused problems
#i believe it was because in an earlier iteration of the code conditions for the recommendation were having some concatenation problem

cclose = float(output.iloc[0]["Close"])
llow = float(min((output["Low"])))
hhigh = float(max((output["High"])))

#variables used in conditions for recommendatioin
lbound = float(0.75)
hbound = float(1.66)

lb2 = (lbound * cclose)
hb2 = (hbound * cclose)

#if statement to create recommendation for whether to buy or not
if llow < lb2 or hhigh > hb2:
    recom = "DO NOT BUY"
    logic = "This stock appears to be very volatile! Unless Jerome Powell is fooling around with interest rates again and causing market-wide turmoil, its best to stay away from this stock for now as it is probably not a bluechip stock!"
else:
    recom = "BUY"
    logic = "This stock does not seem very volatile! You have a high probability of making a profit if you write calls and puts on this company!"


#prints relevant information, prints recommendations
print("LATEST DAILY CLOSING PRICE: $" + dolval(recclose))

print("THE 100-DAY LOW IS : $" + dolval(reclow))
print("THE 100-DAY HIGH IS: $" + dolval(rechigh))




print("")

print("Recommendation: " + recom)
print("Reason for Recommendation: " + logic)

print("")

print("")

print("Thank you for using The Bluechip Stock Picker!")

print("--------------------------------------------------- ")











