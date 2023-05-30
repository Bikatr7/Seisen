## built-in modules
import os
import msvcrt
import time

## third party modules
import keyboard

##-------------------start of read_loop_data()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_loop_data(column) -> int:

    """

    Reads the loop data file and returns the value of the given column\n
    
    Parameters:\n
    column (int) : the column we are reading\n

    Returns:\n
    int(stats[column-1]) : (int) the value of the given column\n

    """

    ## the path to the config directory
    config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

    loop_data_file = os.path.join(config_dir, "loopData.txt")

    with open(loop_data_file, "r", encoding="utf-8") as file:
        loop_data = file.read()

    count = loop_data.count(',')
    i,ii = 0,0
    buildStr = ""
    stats = []

    while(i < count):
        if(loop_data[ii] != ","):
            buildStr += loop_data[ii]
        else:
            stats.append(buildStr)
            buildStr = ""
            i+=1
        ii+=1
        
    return int(stats[column-1])

##--------------------start of input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def input_check(input_type, user_input, number_of_choices, input_prompt_message) -> str:

    """

    Checks the user's input to make sure it is valid for the given input type\n

    Parameters:\n
    input_type (int) : the type of input we are checking\n
    user_input (str) : the user's input\n
    number_of_choices (int) : the number of choices the user has\n
    input_prompt_message (str)  : the prompt to be displayed to the user\n

    Returns:\n
    new_user_input (str) : the user's input\n

    """

    new_user_input = str(user_input)
    input_issue_message = ""

    os.system('cls')

    while(True):

        if(user_input == 'q'):
            exit()

        elif(user_input == 'v' and input_type != 1):
            return new_user_input
        
        elif(input_type == 1 and (str(user_input).isdigit() == False or user_input == "0")):
            input_issue_message = "Invalid Input, please enter a valid number choice or 'q'\n"

        elif(input_type == 4 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices)):
            input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

        elif(input_type == 5 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices)):
            input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

        else:
            return new_user_input

        if(input_type == 5):
            print(input_issue_message + "\n")
            user_input = input(input_prompt_message)

        else:
            print(input_issue_message + "\n" + input_prompt_message)
            user_input = keyboard.read_key()

        os.system('cls')
        clear_stream()

        new_user_input = str(user_input)

##-------------------start-of-clear_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_console() -> None:

    """

    clears the console\n

    Parameters:\n
    None\n

    Returns:\n
    None\n

    """

    os.system('cls' if os.name == 'nt' else 'clear')

##-------------------start-of-pause_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pause_console(message:str="Press enter to continue . . .") -> None:

    """

    pauses the console\n

    Parameters:\n
    message (string) : the message that will be displayed when the console is paused\n

    Returns:\n
    None\n

    """

    if(os.name == 'nt'):  ## Windows
        os.system('pause /P f{message}')
    else: ## Linux
        input(message)

#-------------------Start-of-clear_stream()-------------------------------------------------

def clear_stream(): 

    """

    Clears the console stream\n

    Parameters:\n
    None\n

    Returns:\n
    None\n

    """
    
    while msvcrt.kbhit(): ## while a key is waiting to be read
        msvcrt.getch() ## read the next key and ignore it
        
    time.sleep(0.1) 

#-------------------Start-of-user_confirm()-------------------------------------------------

def user_confirm(prompt):

    """

    Prompts the user to confirm their input\n

    Parameters:\n
    prompt (str) : the prompt to be displayed to the user\n

    Returns:\n
    user_input (str) : the user's input\n

    """

    confirmation = "Just To Confirm You Selected "
    options = " Press 1 To Confirm or 2 To Retry"
    output = ""
    user_input = ""
    
    entry_confirmed = False

    while(entry_confirmed == False):

        os.system('cls')
        
        clear_stream()
        
        user_input = input(prompt)
        
        if(user_input == "q"): ## if the user wants to quit do so
            exit()

        assert user_input != "z" ## z is used to skip

        os.system('cls')

        output = confirmation + user_input + options
        
        print(output)
        
        clear_stream()
        
        if(int(input_check(4, keyboard.read_key(), 2 , output)) == 1):
                entry_confirmed = True
        else:

            os.system('cls')
            
            print(prompt)
    
    os.system('cls')

    return user_input