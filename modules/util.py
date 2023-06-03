## built-in modules
import os
import msvcrt
import time
import typing

##--------------------start-of-input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def input_check(input_type:int, user_input:str, number_of_choices:int, input_prompt_message:str) -> str:

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
            user_input = str(msvcrt.getch().decode())

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
    message (str) : the message that will be displayed when the console is paused\n

    Returns:\n
    None\n

    """

    if(os.name == 'nt'):  ## Windows
        os.system('pause /P f{message}')
    else: ## Linux
        input(message)

##--------------------start-of-clear_stream()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_stream() -> None: 

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

##--------------------start-of-user_confirm()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def user_confirm(prompt:str) -> str:

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
        
        if(int(input_check(4, str(msvcrt.getch()), 2 , output)) == 1):
                entry_confirmed = True
        else:

            os.system('cls')
            
            print(prompt)
    
    os.system('cls')

    return user_input

##--------------------start-of-write_sei_line()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def write_sei_line(sei_file_path:str, items_to_write:typing.List[str]) -> None:

    """
    
    Writes the given items to the given sei file\n

    Parameters:\n
    sei_file_path (str) : the path to the sei file\n
    items_to_write (list - str) : the items to be written to the sei file\n

    Returns:\n
    None\n

    """

    line = ",".join(str(item) for item in items_to_write)
    
    with open(sei_file_path, "a+", encoding="utf-8") as file:
        file.write(line + "," + "\n")

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_sei_line(target_line:int, column_number:int, value_to_replace_to:int, file_path:str) -> None:
    
    """

    Edits the given line in the given file.\n

    Parameters:\n
    target_line (int) : The line number of the file we are editing.\n
    column_number (int) : The column number we are editing.\n
    value_to_replace_to (str) : The value to replace the edit value with.\n
    file_path (str) : The file being edited.\n

    Returns:\n
    None\n

    """
    with open(file_path, "r+", encoding="utf8") as f:
        lines = f.readlines()

    line = lines[target_line - 1]
    items = line.split(",")

    items[column_number - 1] = str(value_to_replace_to)

    new_line = ",".join(items)

    lines[target_line - 1] = new_line + ","

    with open(file_path, "w", encoding="utf8") as file:
        file.writelines(lines)

##-------------------start-of-read_sei_file()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_sei_file(sei_file_path:str, column:int, target_line:int) -> str:

    """

    Reads the given sei file and returns the value of the given column
    
    Parameters:
    sei_file_path (str) : the path to the sei file
    column (int) : the column we are reading

    Returns:
    file_details[column-1] : the value of the given column

    """

    i,ii = 0,0
    build_string = ""
    file_details = []

    with open(sei_file_path, "r", encoding="utf-8") as file:
        sei_file = file.readlines()

    sei_line = sei_file[target_line - 1]

    count = sei_line.count(',')

    while(i < count):
        if(sei_line[ii] != ","):
            build_string += sei_line[ii]
        else:
            file_details.append(build_string)
            build_string = ""
            i+=1
        ii+=1
        
    return file_details[column-1]

##--------------------Start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_new_id(id_list:typing.List[int]) -> int:

    """

    Generate's a new id 

    Parameters:
    id_list (list - string) : a list of already active ids

    Returns:
    new_id (int) : a new id

    """

    id_list = [id for id in id_list]

    new_id = 1

    for num in id_list:
        if(num < new_id):
            continue
        elif(num == new_id):
            new_id += 1
        else:
            return new_id
        
    return new_id

##--------------------Start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def levenshtein(s1, s2):

    """

    Compares two strings for similarity 

    Parameters:
    s1 (string)
    s2 (string)

    Returns:
    distance[sLength1][sLength2] (int) the minimum number of single-character edits required to transform s1 into s2

    """

    sLength1, sLength2 = len(s1), len(s2)
    distance = [[0] * (sLength2 + 1) for _ in range(sLength1 + 1)]
    
    for i in range(sLength1 + 1):
        distance[i][0] = i

    for ii in range(sLength2 + 1):
        distance[0][ii] = ii

    for i in range(1, sLength1 + 1):
        for ii in range(1, sLength2 + 1):

            if(s1[i - 1] == s2[ii - 1]):
                cost = 0
            else:
                cost = 1

            distance[i][ii] = min(distance[i - 1][ii] + 1, distance[i][ii- 1] + 1, distance[i - 1][ii - 1] + cost)

            if(i > 1 and ii > 1 and s1[i-1] == s2[ii-2] and s1[i-2] == s2[ii-1]):
                distance[i][ii] = min(distance[i][ii], distance[i-2][ii-2] + cost)

    return distance[sLength1][sLength2]