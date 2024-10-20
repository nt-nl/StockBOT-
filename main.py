#StockBOT! By Nataniel

import discord
from discord.ext import commands
import yfinance as yf
from datetime import datetime, timedelta

#initialises discord bot (With a prefix for running commands)
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


#Alerts users when the bot is ready
@bot.event
async def on_ready():
    print("StockBOT! Ready")


#Getting Stock Data for the past 30 days
def getStockData(stockTicker):
    
    #This gathers data on the current date, and what date it was 30 days ago
    
    endDate = datetime.now().date()
    startDate = endDate - timedelta(days = 30)


#Downloading Stock Data corresponding with the calculated dates
    stock = yf.download(stockTicker, start = startDate, end = endDate)

    
  #Checks if stock data is available
    if stock.empty:
        return None


#Calculates the information needed.

    CurrentPrice = stock['Close'][-1] #[-1] is used to access the latest Close Price from the end of the list
    LowestPrice = stock['Low'].min()
    HighestPrice = stock['High'].max()
    AveragePrice = stock['Close'].mean() #This means: AveragePrice is the mean of the 'Close' dataFrame in stock (Which is what is holding the information we downloaded to it through yfinance) 

#Returning a dictionary
    return {
       'CurrentPrice': CurrentPrice,
       'LowestPrice': LowestPrice,
       'HighestPrice': HighestPrice,
       'AveragePrice': AveragePrice,
    }



@bot.command()
#When someone types ".hello" in the chat, this function will be performed. "." because of the prefix set at the top.
async def hello(ctx): #ctx (also known as context) is used to reply to messages and more. 
   
    await ctx.send(f"Hi, {ctx.author.mention}. What can I do for you?\n \n **Tip**: use '.ticker **[StockTicker]**' to find out information about that Stock! ")


@bot.command()

#"(ctx, stockTicker: str)" refers to expecting context and then a string which will be recognised as stockTicker in the program
async def ticker(ctx, stockTicker: str):

 stockTicker = stockTicker.upper() #.upper makes sure the ticker is in Capitals
 stockData = getStockData(stockTicker) #Calls the function to download the stock data, with the ticker requested

 if stockData:
   
   await ctx.send(
      f"{ctx.author.mention}:\n"
      f"**Stock Ticker (30 Days)**: {stockTicker}\n"
      f"**Highest Price (30 Days)**: ${stockData['HighestPrice']:.2f}\n" #Accessing the stockData Dictionary
      f"**Average Price (30 Days)**: ${stockData['AveragePrice']:.2f}\n" #:.2f refers to displaying the answer to 2 decimal points
      f"**Lowest Price (30 Days)**: ${stockData['LowestPrice']:.2f}"
   )

 else:
   #Error message if nothing is found for the ticker
   await ctx.send(f"Could not find data for Ticker {stockTicker}")

#Reads the file with the token (for security purposes), IF SOMEONE WANTS TO USE THIS BOT COPY YOUR TOKEN INTO "token.txt"
f = open("token.txt", "r")
token = f.readline()
f.close

bot.run(token)
