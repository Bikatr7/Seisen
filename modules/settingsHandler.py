## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

class settingsHandler():

    """
    
    The handler that handles all of Seisen's settings
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, local_handler:localHandler, remote_handler:remoteHandler) -> None:

        """
        
        Initializes the settingsHandler class.\n

        Parameters:\n
        self (object - settingsHandler) : The settings handler object.\n
        local_handler (object - localHandler) : The local handler object.\n
        remote_handler (object - remoteHandler) : The remote handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.local_handler = local_handler

        self.remote_handler = remote_handler

##--------------------start-of-change_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
