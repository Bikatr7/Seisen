## built-in imports
import datetime
import os

class logger:

    '''

    The logger class is used to log actions taken by Seisen.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_log_file_path:str):

        """
        
        Initializes a new logger object.\n

        Parameters:\n
        self (object - logger) : The csep object to be initialized.\n
        incoming_log_file_path (str) : The path to the log file.\n

        Returns:\n
        None.\n

        """

        self.log_file_path = incoming_log_file_path

##--------------------start-of-get_time_stamp()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_time_stamp(self):

        """
        
        gets the time stamp for a logging action taken.\n

        Parameters:\n
        self (object - logger) : The logger object.\n

        Returns:\n
        time_stamp

        """


        current_date = datetime.date.today().strftime("%Y-%m-%d")

        current_time = datetime.datetime.now().time().strftime("%H:%M:%S")

        time_stamp = "(" + current_date + " " + current_time + ") : "

        return time_stamp
    
##--------------------start-of-log_action()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def log_action(self, action:str):

        """
        
        Logs an action.\n

        Parameters:\n
        self (object - logger) : the logger object.\n
        action (str) : the action being logged.\n

        Returns:\n
        None.\n
 
        """

        time_stamp = self.get_time_stamp()

        with open(self.log_file_path, 'a+', encoding="utf-8") as file:
            file.write(time_stamp + action + "\n")