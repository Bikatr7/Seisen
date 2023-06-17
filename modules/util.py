## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things
from datetime import datetime

import os
import msvcrt
import time
import typing

## custom modules
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.localHandler import localHandler
    from modules.words import word

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

        clear_console()
        
        clear_stream()
        
        user_input = input(prompt)
        
        if(user_input == "q"): ## if the user wants to quit do so
            exit()

        assert user_input != "z" ## z is used to skip

        clear_console()

        output = confirmation + user_input + options
        
        print(output)
        
        clear_stream()
        
        if(int(input_check(4, str(msvcrt.getch()), 2 , output)) == 1):
                entry_confirmed = True
        else:

            clear_console()

            print(prompt)
    
    clear_console()

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

def edit_sei_line(file_path:str, target_line:int, column_number:int, value_to_replace_to:int) -> None:
    
    """

    Edits the given line in the given file.\n

    Parameters:\n
    file_path (str) : The file being edited.\n
    target_line (int) : The line number of the file we are editing.\n
    column_number (int) : The column number we are editing.\n
    value_to_replace_to (str) : The value to replace the edit value with.\n

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

def read_sei_file(sei_file_path:str, target_line:int, column:int) -> str:

    """

    Reads the given sei file and returns the value of the given column\n
    
    Parameters:\n
    sei_file_path (str) : the path to the sei file\n
    target_line (int) : the line number of the sei file
    column (int) : the column we are reading\n

    Returns:\n
    file_details[column-1] : the value of the given column\n

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

##--------------------start-of-get_new_id()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_new_id(id_list:typing.List[int]) -> int:

    """

    Generate's a new id\n 

    Parameters:\n
    id_list (list - string) : a list of already active ids\n

    Returns:\n
    new_id (int) : a new id\n

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

##--------------------start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def levenshtein(string_one:str, string_two:str) -> int:

    """

    Compares two strings for similarity\n

    Parameters:\n
    string_one (str) : the first string to compare\n
    string_two (str) : the second string to compare\n

    Returns:\n
    distance[sLength1][sLength2] (int) : the minimum number of single-character edits required to transform string_one into string_two\n

    """

    sLength1, sLength2 = len(string_one), len(string_two)
    distance = [[0] * (sLength2 + 1) for _ in range(sLength1 + 1)]
    
    for i in range(sLength1 + 1):
        distance[i][0] = i

    for ii in range(sLength2 + 1):
        distance[0][ii] = ii

    for i in range(1, sLength1 + 1):
        for ii in range(1, sLength2 + 1):

            if(string_one[i - 1] == string_two[ii - 1]):
                cost = 0
            else:
                cost = 1

            distance[i][ii] = min(distance[i - 1][ii] + 1, distance[i][ii- 1] + 1, distance[i - 1][ii - 1] + cost)

            if(i > 1 and ii > 1 and string_one[i-1] == string_two[ii-2] and string_one[i-2] == string_two[ii-1]):
                distance[i][ii] = min(distance[i][ii], distance[i-2][ii-2] + cost)

    return distance[sLength1][sLength2]

##--------------------start-of-check_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_typo(word:word, user_guess:str, prompt:str, handler:localHandler) -> str:  

    """

    checks if a user_guess is a typo or not\n

    Parameters:\n
    word (object - word) : the word we're checking typos for\n
    user_guess (str) : the user's guess\n
    prompt (str) : the prompt that was given to the user\n
    handler (object - localHandler) : the local handler
    
    Returns:\n
    final_answer (string) the user's final answer after being corrected for typos\n

    """

    min_distance = 3
    final_answer = user_guess

    if(user_guess in word.typos):
        return [item for item in word.typos if item == user_guess][0]
    elif(user_guess in word.incorrect_typos):
        return user_guess

    for correct_answer in word.testing_material_answer_all:

        distance = levenshtein(user_guess, correct_answer)

        if(distance < min_distance):

            print("\nDid you mean : " + correct_answer + "? Press 1 to Confirm or 2 to Decline.\n")
        
            userA = int(input_check(1 ,str(msvcrt.getch().decode()), 2, prompt + "\nDid you mean : " + correct_answer + "? Press 1 to Confirm or 2 to Decline.\n"))
        
            clear_console()

            if(userA == 1):

                final_answer = correct_answer

                word.log_new_typo(user_guess, handler)

                return final_answer

    word.log_new_incorrect_typo(user_guess, handler)
    
    return final_answer

##--------------------start-of-standard_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def standard_create_directory(directory_path:str):

    """

    Creates a directory if it doesn't exist, as well as prints to console what was created, along with a slight delay.\n

    Parameters:\n
    directory_path (str) : path to the directory to be created.\n

    Returns:\n
    None\n

    """

    if(os.path.isdir(directory_path) == False):
        os.mkdir(directory_path)
        print(directory_path + " created due to lack of the folder")
        time.sleep(0.1)

##--------------------start-of-modified_create_directory()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def modified_create_directory(directory_path:str, path_to_check:str):

    """

    Creates a directory if it doesn't exist or if the path provided is blank or empty, as well as prints to console what was created, along with a slight delay.\n

    Parameters:\n
    directory_path (str) : path to the directory to be created.\n
    path_to_check (str) : path to check if it is blank\n

    Returns:\n
    None\n

    """

    if(os.path.isdir(directory_path) == False or os.path.getsize(path_to_check) == 0):
        os.mkdir(directory_path)
        print(directory_path + " created due to lack of the folder or " + path_to_check + " was blank or empty")
        time.sleep(0.1)

##--------------------start-of-standard_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def standard_create_file(file_path:str):

    """

    Creates a file if it doesn't exist, truncates it,  as well as prints to console what was created, along with a slight delay.\n

    Parameters:\n
    file_path (str) : path to the file to be created.\n

    Returns:\n
    None\n

    """

    if(os.path.exists(file_path) == False):
        print(file_path + " was created due to lack of the file")
        with open(file_path, "w+", encoding="utf-8") as file:
            file.truncate()

##--------------------start-of-modified_create_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def modified_create_file(file_path:str, content_to_write:str):

    """

    Creates a path if it doesn't exist or if it is blank or empty, writes to it,  as well as prints to console what was created, along with a slight delay.\n

    Parameters:\n
    file_path (str) : path to the file to be created.\n
    content to write (str) : content to be written to the file\n

    Returns:\n
    None\n

    """

    if(os.path.exists(file_path) == False or os.path.getsize(file_path) == 0):
        print(file_path + " was created due to lack of the file or because it is blank")
        with open(file_path, "w+", encoding="utf-8") as file:
            file.write(content_to_write)

##--------------------start-of-create_archive_dir()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_archive_dir(type_of_archive:int):

    """
    
    Creates the archive directory based on the given type of archive\n

    Parameters:\n
    type_of_archive (int) : The type of archive\n

    Returns:\n
    archive_directory (str) : The path to the newly created archive directory\n

    """

    ##----------------------------------------------------------------dirs----------------------------------------------------------------

    ## the folder where all the config files are located
    config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

    ## archives for previous versions of Seisen txt files
    archives_dir = os.path.join(config_dir, "Archives")

    ## archives for the database files
    database_archives_dir = os.path.join(archives_dir, "Database")

    ## archives for the local files
    local_archives_dir = os.path.join(archives_dir, "Local")

    ##----------------------------------------------------------------other things----------------------------------------------------------------
    
    current_day = datetime.today().strftime('%Y-%m-%d')

    filePaths = {
        1: database_archives_dir,
        2: local_archives_dir
    }

    archive_directory = os.path.join(filePaths[type_of_archive], current_day)

    standard_create_directory(archive_directory)

    return archive_directory