## custom modules

from modules.logger import logger
from modules.fileEnsurer import fileEnsurer
from modules.toolkit import toolkit

class settingsHandler():

    """
    
    The handler that handles all of Seisen's settings
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, logger:logger, toolkit:toolkit) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        logger (object - logger) : The logger object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------
        
        self.fileEnsurer = file_ensurer

        self.logger = logger

        self.toolkit = toolkit