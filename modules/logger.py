## build-in libraries
from datetime import datetime


class Logger:

    """
    
    The logger class is used to log actions taken by Seisen.

    """

    log_file_path = ""

    current_batch = ""
    
##--------------------start-of-log_action()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_action(action:str, output:bool=False, omit_timestamp:bool=False, is_error:bool=False) -> str:

        """
        
        Logs an action.

        Parameters:
        action (str) : the action being logged.
        output (bool | optional | defaults to false) : whether or not to output the action to the console.
        omit_timestamp (bool | optional | defaults to false) : whether or not to omit the timestamp from the action.
        is_error (bool | optional | defaults to false) : whether or not the action is an error.
 
        """

        timestamp = Logger.get_timestamp() 

        log_line = timestamp + action + "\n"

        Logger.current_batch += log_line

        if(omit_timestamp):
            log_line = action

        if(output):
            print(log_line)

        if(is_error):
            return timestamp + log_line
        
        return ""

##--------------------start-of-log_barrier()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def log_barrier() -> None:
            
        """
        
        Logs a barrier.

        """
    
        Logger.log_action("-------------------------")

##--------------------start-of-push_batch()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def push_batch() -> None:

        """
        
        Pushes all stored actions to the log file.

        """

        with open(Logger.log_file_path, 'a+', encoding="utf-8") as file:
            file.write(Logger.current_batch)

##--------------------start-of-clear_batch()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_batch() -> None:

        """
        
        Clears the current batch.

        """

        Logger.current_batch = ""
        
##--------------------start-of-clear_log_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_log_file() -> None:

        """
        
        Clears the log file.
        
        """

        with open(Logger.log_file_path, 'w+', encoding="utf-8") as file:
            file.truncate(0)

##-------------------start-of-get_timestamp()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_timestamp() -> str:

        """
        
        Generates a timestamp for an action taken by Kudasai.

        Returns:
        time_stamp (string) : The timestamp for the action.        
        
        """

        time_stamp = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "

        return time_stamp