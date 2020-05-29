## DnD Dice Roller
from random import randint
from os import system
import cmd2

class DiceRoller(cmd2.Cmd):

    completekey = 'tab'
    intro = 'Welcome to Dice Roller. Enter help for a list of commands.\n'
    prompt = 'DnD % '
    file = None

    def do_exit(self, arg):
        print('See ya next time!\n')
        return True
    
    def do_quit(self, arg):
        return self.do_exit(arg)

    def do_test(self, arg):
        print(*parse(arg))

    def do_EOF(self, arg):
        print('\nSee ya next time!\n')
        return True

    def default(self, arg):
        print(arg)
        debug(arg)
        initiate_roll(arg)

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

if __name__ == '__main__':
    DiceRoller().cmdloop()
