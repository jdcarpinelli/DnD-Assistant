## DnD Dice Roller
from random import randint
from os import system

# List of acceptable rolls
__dnd_die = [4, 6, 8, 10, 12, 20]

# Error messages
INVALID_DIE = 'Only 4, 6, 8, 10, 12, or 20 sided die can be rolled!'
INVALID_ARG = ''


def roll_request(args):

    ## First assume 1 arg

    # If form '3d6'
    if 'd' in args[0]:

        first_cmd = str(args[0]).split('d')

        # Wrong usage, this should never actually run
        if len(first_cmd) != 2:
            return False, ''
        
        # Otherwise, if length of 2
        else:
            # Wrong usage cases ('#d', 'd')
            if first_cmd[1] == '':
                return False, INVALID_ARG
            else:
                # If no num_dice given, assume 1
                if first_cmd[0] == '':
                    num_die = 1
                else:
                    # Both number of die and die type are given
                    num_die = int(first_cmd[0])

                die_num = int(first_cmd[1])

                if die_num not in __dnd_die:
                    return False, INVALID_DIE
                else:
                    return(
                        roll(num_die, die_num)
                    )
    else:
        # If not only numbers
        if not all(char.isdigit() for char in args[0]):
            return False, INVALID_ARG
        
        # Otherwise, if command is only a number
        else:
            # Assume 1 die
            num_die = 1
            die_num = int(args[0])
            
            if die_num not in __dnd_die:
                return False, INVALID_DIE
            else:
                return(
                    roll(num_die, die_num)
                )



def roll(num_die, die_num):
    roll_str =''
    for die in range(num_die - 1):
        roll_str += (str(randint(1,die_num)) + ', ')
    roll_str += str(randint(1, die_num))
    return True, roll_str

