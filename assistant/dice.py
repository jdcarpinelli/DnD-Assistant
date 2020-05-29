## DnD Dice Roller
from random import randint
from os import system


def debug(arg):
    print('Arguments: ', *parse(arg), '\n')

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(arg.split())

def initiate_roll(arg_list):
    print(parse(arg_list))

def roll(self, arg):
    rolls = []
    for die in range(num_dice):
        rolls.append(randint(1,n))

    return rolls

def roll_to_str(self, arg):
    roll_str = ''
    for die in range(len(num_list) - 1):
        roll_str += (str(num_list[die]))
        roll_str += (', ')
    
    roll_str += (str(num_list[-1]))
    return roll_str