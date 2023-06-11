## built-in modules
import os
import typing

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint
from modules.words import word as kana_blueprint
from modules import util


class localHandler():

    """
    
    The handler that handles the connection to local storage and all interactions with it.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """
        
        The __init__() method initializes the remoteHandler class\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        ## the path to the config directory
        self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        ## the path to the file that stores the password
        self.password_file = os.path.join(os.path.join(self.config_dir, "Logins"), "credentials.txt")

        ## the paths to the file that stores the kana words and its typos
        self.kana_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana.txt")
        self.kana_typos_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana typos.txt")
        self.kana_incorrect_typos_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana incorrect typos.txt")

        ## the kana that seisen will use to test the user
        self.kana = [] 

        ## the literal used in the database to flag words as Kana
        self.KANA_WORD_TYPE = "2"

        ## the accepted typos for kana
        self.kana_typos = []

        ## the accepted incorrect typos for kana
        self.kana_incorrect_typos = []

##--------------------start-of-load_words_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def load_words_from_local_storage(self) -> None:
        
        """
        
        loads the words from the local storage\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        KANA_TYPO_WORD_ID_INDEX_LOCATION = 0
        KANA_TYPO_TYPO_ID_INDEX_LOCATION = 1
        KANA_TYPO_VALUE_INDEX_LOCATION = 2
        KANA_TYPO_WORD_TYPE_INDEX_LOCATION = 3
        


        self.kana.clear()

        with open(self.kana_file, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                self.kana.append(kana_blueprint(int(values[0]), values[1], values[2], [], int(values[3]), int(values[4])))

        with open(self.kana_typos_file, "r", encoding="utf-8") as file:

            for line in file:
                
                values = line.strip().split(',')

                if(int(values[0]) == self.KANA_WORD_TYPE):
                    for kana in self.kana:
                        if(kana.word_id == int(values[1])):
                            kana.typos.append(typo_blueprint(int(values[0]), int(values[1]), int(values[2]), values[4]))

        with open(self.kana_incorrect_typos_file, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                if(int(values[0]) == self.KANA_WORD_TYPE):
                    for kana in self.kana:
                        if(kana.word_id == int(values[1])):
                            kana.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), int(values[2]), values[4]))

##--------------------start-of-get_list_of_all_ids()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_list_of_all_ids(self, type_of_id_to_query:int) -> typing.List[int]:

        """

        Gets the list of all ids in the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        ids (list - string) : The list of all ids in the database\n

        """

        ids = ["0"]

        i = 0

        TYPO_ID_IDENTIFIER = 1
        INCORRECT_TYPO_ID_IDENTIFIER = 2

        if(type_of_id_to_query == TYPO_ID_IDENTIFIER):
            with open(self.kana_typos_file, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.kana_typos_file,i+1,2))
                    i+=1

        elif(type_of_id_to_query == INCORRECT_TYPO_ID_IDENTIFIER):
            with open(self.kana_incorrect_typos_file, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.kana_incorrect_typos_file,i+1,2))
                    i+=1



        ids =  [int(x) for x in ids]


        return ids