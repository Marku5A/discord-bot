import stocks


user_list = []
username_list = {}
import mysql.connector

mydb = mysql.connector.connect(
    host="xxxx",
    user="xxxx",
    passwd="xxxx",
    database="xxxx"
)
mycursor = mydb.cursor()

class user():
    name = ""
    username = ""
    stocks = 0
    balance = 0
    nope = False

    def __init__(self, name, username, stocks, balance):
        self.name = name
        self.username = username
        self.stocks = stocks
        self.balance = balance
        self.nope = False

        sql = "INSERT INTO users (name, id, stocks, balance) VALUES (%s, %s, %s, %s)"

    def buy_stocks(self, stock_amount):
        price = stocks.stock1.value * stock_amount
        if (price > self.balance):
            self.nope = True
        else:
            stocks.stock1.num_stocks -= stock_amount
            self.stocks += stock_amount
            self.balance -= price

    def sell_stocks(self, stock_amount):
        price = stocks.stock1.value * stock_amount
        if (self.stocks < stock_amount):
            self.nope = True
        else:
            stocks.stock1.num_stocks += stock_amount
            self.stocks -= stock_amount
            self.balance += price
            
