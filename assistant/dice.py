## DnD Dice Roller
from random import randint
from os import system

# List of acceptable rolls
dnd_die = [4, 6, 8, 10, 12, 20]

def initiate_roll(args):
    ret_str = ''
    for arg in args:
        ret_str += arg + ', '
    return ret_str
    
def roll(num_die, die_num):
    roll_str = []
    for die in range(1, num_die):
        roll_str += str(randint(1,die_num))
    return roll_str

