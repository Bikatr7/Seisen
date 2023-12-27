## built-in modules
import os
import time
import typing

## custom modules
from modules.file_ensurer import FileEnsurer

class Toolkit():

    """
    
    The class for a bunch of utility functions used throughout Seisen.

    """

    CURRENT_VERSION = "v2.1.0"

##--------------------start-of-input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def input_check(input_type:int, user_input:str, number_of_choices:int, input_prompt_message:str) -> str:

        """

        Checks the user's input to make sure it is valid for the given input type.

        Parameters:
        input_type (int) : the type of input we are checking.
        user_input (str) : the user's input.
        number_of_choices (int) : the number of choices the user has.
        input_prompt_message (str)  : the prompt to be displayed to the user.

        Returns:
        new_user_input (str) : the user's input.

        """

        new_user_input = str(user_input)
        input_issue_message = ""

        Toolkit.clear_console()

        while(True):

            if(user_input == 'q'):
                FileEnsurer.exit_seisen()

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
                user_input = Toolkit.get_single_key()

            Toolkit.clear_console()
            Toolkit.clear_stream()

            new_user_input = str(user_input)

##--------------------start-of-get_user_input()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_single_key() -> str:

        """

        Gets a single key from the user.

        Returns:
        user_input (str) : the user's input.

        """

        if(os.name == 'nt'):  ## Windows

            import msvcrt

            user_input = str(msvcrt.getch().decode())
            
        else:  ## Linux

            import sys
            import termios
            import tty

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                user_input = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return user_input

##-------------------start-of-clear_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_console() -> None:

        """

        Clears the console.

        """

        os.system('cls' if os.name == 'nt' else 'clear')

##-------------------start-of-pause_console()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def pause_console(message:str="Press any key to continue...") -> None:

        """

        Pauses the console.

        Parameters:
        message (str | optional) : the message that will be displayed when the console is paused.

        """

        print(message)  ## Print the custom message
        
        if(os.name == 'nt'):  ## Windows

            import msvcrt
            
            msvcrt.getch() 

        else:  ## Linux

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

##-------------------start-of-maximize_window()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def maximize_window():

        """
        
        Maximizes the console window.

        """

        try:

            if(os.name == 'nt'):

                import ctypes

                ## Get the handle of the console window
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()

                ## Maximize the console window
                ctypes.windll.user32.ShowWindow(hwnd, 3)

            else:
                print("\033[8;40;140t")

        except:
            pass

##-------------------start-of-minimize_window()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def minimize_window():

        """
        
        Minimizes the console window.

        """

        try:

            if(os.name == 'nt'):

                import ctypes

                ## Get the handle of the console window
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()

                ## Maximize the console window
                ctypes.windll.user32.ShowWindow(hwnd, 9)

            elif(system_name == "Linux"):
                print("\033[8;25;80t")

        except:
            pass
                
##--------------------start-of-clear_stream()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_stream() -> None: 

        """

        Clears the console stream.

        ## need to make this work on linux and mac

        """

        try:

            if(os.name == 'nt'):

                import msvcrt
        
                while msvcrt.kbhit(): ## while a key is waiting to be read
                    msvcrt.getch() ## read the next key and ignore it

            else:

                import sys
                import termios
                import tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd, termios.TCSANOW)
                    termios.tcflush(fd, termios.TCIFLUSH)
                finally:
                    termios.tcsetattr(fd, termios.TCSANOW, old_settings)

            time.sleep(0.1) 

        except:
            pass

##--------------------start-of-user_confirm()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def user_confirm(prompt:str) -> str:

        """

        Prompts the user to confirm their input.

        Parameters:
        prompt (str) : the prompt to be displayed to the user.\n

        Returns:
        user_input (str) : the user's input.

        """

        confirmation = "Just To Confirm You Selected "
        options = " (Press 1 To Confirm, 2 To Retry, z to skip, or q to quit)\n"
        output = ""
        user_input = ""
        
        entry_confirmed = False

        while(entry_confirmed == False):

            Toolkit.clear_console()
            
            Toolkit.clear_stream()
            
            user_input = input(prompt + options)
            
            if(user_input == "q"): ## if the user wants to quit do so
                FileEnsurer.exit_seisen()

            if(user_input == "z"): ## z is used to skip
                raise Toolkit.UserCancelError()

            Toolkit.clear_console()

            output = confirmation + user_input + options
            
            print(output)
            
            Toolkit.clear_stream()
            
            if(int(Toolkit.input_check(4, Toolkit.get_single_key(), 2 , output)) == 1):
                    entry_confirmed = True
            else:

                Toolkit.clear_console()

                print(prompt)
        
        Toolkit.clear_console()

        return user_input

##-------------------start-of-check_update()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def check_update() -> typing.Tuple[bool, str]:

        """

        Determines if Seisen has a new latest release, and confirms if an internet connection is present or not.
        If requests is not installed, it will return is_connection as False.

        Returns:
        is_connection (bool) : Whether or not the user has an internet connection.
        update_prompt (str) : The update prompt to be displayed to the user, can either be blank if there is no update or contain the update prompt if there is an update.

        """

        update_prompt = ""
        is_connection = True

        try:

            import requests

            response = requests.get("https://api.github.com/repos/Bikatr7/Seisen/releases/latest")
            latest_version = response.json()["tag_name"]
            release_notes = response.json()["body"]

            if(latest_version != Toolkit.CURRENT_VERSION):
                update_prompt += "There is a new update for Seisen (" + latest_version + ")\nIt is recommended that you use the latest version of Seisen\nYou can download it at https://github.com/Bikatr7/Seisen/releases/latest \n"

                if(release_notes):
                    update_prompt += "\nRelease notes:\n\n" + release_notes + '\n'

            return is_connection, update_prompt

        ## used to determine if user lacks an internet connection or possesses another issue that would cause the automated mtl to fail.
        except ImportError:

            print("Requests is not installed, please install it using the following command:\npip install requests")

            Toolkit.pause_console()

            is_connection = False

            return is_connection, update_prompt

        except Exception as e:

            is_connection = False

            return is_connection, update_prompt
    
##--------------------start-of-UserCancelError------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    class UserCancelError(Exception):

        """
        
        Is raised when a user cancel's an action.

        """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        def __init__(self):

            """
            
            Initializes a new UserCancelError Exception.

            """

            self.message = "User Canceled."