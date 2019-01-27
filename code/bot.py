# bot.py
import discord
import requests
import json
import random
import stocks
import users
import mysql.connector

#Connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="xxxx",
    passwd="xxxx",
    database="xxxx"
)
mycursor = mydb.cursor()

N = 0
# command handler class

class CommandHandler:

    # constructor
    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                            break
                        else:
                            return self.client.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(command['trigger'], command['args_num'], ', '.join(command['args_name'])))
                            break
                else:
                    break


# create discord client
client = discord.Client()
token = 'xxxxx'

# create the CommandHandler object and pass it the client
ch = CommandHandler(client)

## start commands command
def commands_command(message, client, args):
    try:
        count = 1
        coms = '**Commands List**\n'
        for command in ch.commands:
            coms += '{}) `{}` : {}\n'.format(count, command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!commands',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints a list of all the commands!'
})
## end commands command

## start print db command
def db_command(message, client, args):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        for x in mycursor:
            return x
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!dbinfo',
    'function': db_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints the info of the database!'
})
## end print stocks command

## start print stocks command
def stock_command(message, client, args):
    try:
        text  = '***'+str(stocks.stock1.name)+'***\nValue:\n`$'+str(stocks.stock1.value)+'`\nAmount:\n`'+str(stocks.stock1.num_stocks)+'`'
        return text
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!stockinfo',
    'function': stock_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints the info of a stock!'
})
## end print stocks command

## start change stocks command
def change_stock_command(message, client, args):
    try:
        stocks.stock1.change_stocks()
        change_text  = '***New '+str(stocks.stock1.name)+' Value:***\n$`' + str(stocks.stock1.value)+'`'
        return change_text
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!stockchange',
    'function': change_stock_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Changes the value of a stock!'
})
## end change stocks command

## start create user command
def create_user(message, client, args):
    try:
        global N
        users.user_list.append(users.user(str(args[0]), message.author, 0, 150))
        textout = '***Created New User *** ` '+str(users.user_list[0].name)+'`\nCurrent user is ` '+str(users.user_list[0].username)+'`'
        users.username_list[str(message.author)] = N
        N += 1
        return textout
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!createuser',
    'function': create_user,
    'args_num': 1,
    'args_name': [],
    'description': 'Creates a new user!'
})
## end create user command

## start buy stocks command
def buy_stocks(message, client, args):
    try:
        theprice = str(stocks.stock1.value * int(args[0]))
        X = 0
        X = users.username_list[str(message.author)]
        users.user_list[X].buy_stocks(int(args[0]))
        if (users.user_list[X].nope):
            textoutput = '***You Don\'t Have Enough Money To Do That!***\nThe price of ` '+str(args[0])+' ` Stocks is ` $'+theprice+'`!\nYou only have ` $'+str(users.user_list[X].balance)+'`'
            users.user_list[X].nope = False
        else:
            textoutput = '***Bought *** ` '+str(args[0])+'` ***Stocks for *** $` '+theprice+'`'
        return textoutput
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!buystocks',
    'function': buy_stocks,
    'args_num': 1,
    'args_name': [],
    'description': 'Buys a certain amount of stocks!'
})
## end buy stocks command

## start sell stocks command
def sell_stocks(message, client, args):
    try:
        theprice = str(stocks.stock1.value * int(args[0]))
        X = 0
        X = users.username_list[str(message.author)]
        users.user_list[X].sell_stocks(int(args[0]))
        if (users.user_list[X].nope):
            textoutput = '***You Don\'t Have Enough Stocks To Do That!***\nYou\'re Trying to Sell ` '+str(args[0])+' ` Stocks, You only have ` '+str(users.user_list[X].stocks)+' ` Stocks!'
            users.user_list[X].nope = False
        else:
            textout = '***Sold *** ` '+str(args[0])+'` ***Stocks for *** $` '+theprice+'`'
        return textout
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!sellstocks',
    'function': sell_stocks,
    'args_num': 1,
    'args_name': [],
    'description': 'Sells a certain amount of stocks!'
})
## end sell stocks command


## start user info command
def user_info(message, client, args):
    try:
        X = 0
        X = users.username_list[str(message.author)]
        output = '***User *** ` '+str(users.user_list[X].name)+'`\'s *** Info: ***\n`'+str(users.user_list[X].stocks)+' ` Stocks Bought\n$`'+str(users.user_list[X].balance)+'`'
        return output
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!userinfo',
    'function': user_info,
    'args_num': 0,
    'args_name': [],
    'description': 'Lists info about the user!'
})
## end user info command

# bot is ready
@client.event
async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)

# on new message
@client.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == client.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print(e)

# start bot
client.run(token)
