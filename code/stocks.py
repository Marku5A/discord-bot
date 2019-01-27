import random
from time import sleep

class stocks():
    value = 10
    up_down = [True, False]
    min_change = 0.10
    max_change = 0.50
    num_stocks = 100
    
    def __init__(self, name, min_change, max_change, num_stocks):
        self.name = name
        self.min_change = min_change
        self.max_change = max_change
        self.num_stocks = num_stocks

    def change_stocks(self):
        add_sub = random.choice(self.up_down)
        change = round(random.uniform(self.min_change, self.max_change), 2)
        if add_sub:
            self.value += change
        else:
            self.value -= change

stock1 = stocks("Stock_1", 0.10, 0.50, 100)
