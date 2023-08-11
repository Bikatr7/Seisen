## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things

import os
import msvcrt
import time
import typing
import requests

## custom modules
if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from modules.logger import logger

class toolkit():

    """
    
    The class for a bunch of utility functions used throughout Seisen.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, logger:logger) -> None:

        """
        
        Initializes the toolkit class.\n

        Parameters:\n
        logger (object - logger) : The logger object.\n

        Returns:\n
        None.\n

        """

        self.logger = logger

##--------------------start-of-input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def input_check(self, input_type:int, user_input:str, number_of_choices:int, input_prompt_message:str) -> str:

        """

        Checks the user's input to make sure it is valid for the given input type.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n
        input_type (int) : the type of input we are checking.\n
        user_input (str) : the user's input.\n
        number_of_choices (int) : the number of choices the user has.\n
        input_prompt_message (str)  : the prompt to be displayed to the user.\n

        Returns:\n
        new_user_input (str) : the user's input.\n

        """

        new_user_input = str(user_input)
        input_issue_message = ""

        self.clear_console()

        while(True):

            if(user_input == 'q'):
                self.exit_seisen()

            elif(user_input == 'v' and input_type != 1):
                return new_user_input
            
            elif(input_type == 1 and (str(user_input).isdigit() == False or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q'\n"

            elif(input_type == 4 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

            elif(input_type == 5 and (str(user_input).isdigit() == False or int(user_input) > number_of_choices or user_input == "0")):
                input_issue_message = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"

            else:
                return new_user_input

            if(input_type == 5):
                print(input_issue_message + "\n")
                user_input = input(input_prompt_message)

            elif(input_type == 4 or input_type == 1):
                print(input_issue_message + "\n" + input_prompt_message)
                user_input = str(msvcrt.getch().decode())

            self.clear_console()
            self.clear_stream()

            new_user_input = str(user_input)

##-------------------start-of-clear_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_console(self) -> None:

        """

        clears the console.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        os.system('cls' if os.name == 'nt' else 'clear')

##-------------------start-of-pause_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def pause_console(self, message:str="Press any key to continue...") -> None:

        """

        pauses the console.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n
        message (str - optional) : the message that will be displayed when the console is paused.\n

        Returns:\n
        None\n

        """

        print(message)  # Print the custom message
        
        if(os.name == 'nt'):  ## Windows
            
            msvcrt.getch() 

        else:  ## Linux, No idea if any of this works lmao

            import termios

            ## Save terminal settings
            old_settings = termios.tcgetattr(0)

            try:
                new_settings = termios.tcgetattr(0)
                new_settings[3] = new_settings[3] & ~termios.ICANON
                termios.tcsetattr(0, termios.TCSANOW, new_settings)
                os.read(0, 1)  ## Wait for any key press

            finally:

                termios.tcsetattr(0, termios.TCSANOW, old_settings)
                
##--------------------start-of-clear_stream()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clear_stream(self) -> None: 

        """

        Clears the console stream.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """
        
        while msvcrt.kbhit(): ## while a key is waiting to be read
            msvcrt.getch() ## read the next key and ignore it
            
        time.sleep(0.1) 

##--------------------start-of-user_confirm()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def user_confirm(self, prompt:str) -> str:

        """

        Prompts the user to confirm their input.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n
        prompt (str) : the prompt to be displayed to the user.\n

        Returns:\n
        user_input (str) : the user's input.\n

        """

        confirmation = "Just To Confirm You Selected "
        options = " (Press 1 To Confirm, 2 To Retry, z to skip, or q to quit)\n"
        output = ""
        user_input = ""
        
        entry_confirmed = False

        while(entry_confirmed == False):

            self.clear_console()
            
            self.clear_stream()
            
            user_input = input(prompt + options)
            
            if(user_input == "q"): ## if the user wants to quit do so
                self.exit_seisen()

            if(user_input == "z"): ## z is used to skip
                raise self.UserCancelError()

            self.clear_console()

            output = confirmation + user_input + options
            
            print(output)
            
            self.clear_stream()
            
            if(int(self.input_check(4, str(msvcrt.getch().decode()), 2 , output)) == 1):
                    entry_confirmed = True
            else:

                self.clear_console()

                print(prompt)
        
        self.clear_console()

        return user_input

##-------------------start-of-check_update()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_update(self) -> bool:

        """

        determines if Seisen has a new latest release, and confirms if an internet connection is present or not.\n

        Parameters:\n
        self (object - toolkit) : The toolkit object.\n

        Returns:\n
        True if the user has an internet connection, False if the user does not.\n

        """
        
        try:

            self.clear_console()
        
            CURRENT_VERSION = "v1.2.0" 

            response = requests.get("https://api.github.com/repos/Seinuve/Seisen/releases/latest")
            latest_version = response.json()["tag_name"]
            release_notes = response.json()["body"]

            self.logger.log_action("Current Version: " + CURRENT_VERSION)

            if(latest_version != CURRENT_VERSION):
                print("There is a new update for Seisen (" + latest_version + ") Currently on (" + CURRENT_VERSION + ")\nIt is recommended that you use the latest version of Seisen\nYou can download it at https://github.com/Seinuve/Seisen/releases/latest \n")
                self.logger.log_action("Prompted Update Request for " + latest_version)

                if(release_notes):
                    print("Release notes:\n\n" + release_notes + '\n')

                self.pause_console()
                self.clear_console()

            return True

        except: ## used to determine if user lacks an internet connection or possesses another issue that would cause any internet related functionalities to fail
                    
            return False
    
##--------------------start-of-exit_seisen()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def exit_seisen(self):

        """
        
        Pushes the log batch to the log and exits.\n

        Parameters:\n
        self (object - toolkit) : the toolkit object.\n

        Returns:\n
        None.\n

        """

        self.logger.push_batch()

        exit()

##--------------------start-of-UserCancelError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    class UserCancelError(Exception):

        """
        
        Is raised when a user cancel's an action\n

        """


##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        def __init__(self):

            """
            
            Initializes a new UserCancelError Exception.\n

            Parameters:\n
            None.\n

            Returns:\n
            None.\n

            """

            self.message = "User Canceled."