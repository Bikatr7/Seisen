## built-in imports
import datetime

class logger:

    '''

    The logger class is used to log actions taken by Seisen.\n
        
    '''

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def __init__(self, incoming_log_file_path:str):

        """
        
        Initializes a new logger object.\n

        Parameters:\n
        self (object - typo) : The csep object to be initialized.\n
        incoming_log_file_path (str) : The path to the log file.\n

        Returns:\n
        None.\n

        """

        self.log_file_path = incoming_log_file_path


##--------------------start-of-get_time_stamp()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_time_stamp(self):


        current_date = datetime.date.today().strftime("%Y-%m-%d")

        current_time = datetime.datetime.now().time().strftime("%H:%M:%S")

        return "(" + current_date + " " + current_time + ")"