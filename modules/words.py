## built-in modules
import typing
import msvcrt

## custom modules
from modules import util

class word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class

    Kana also uses this class.
    
    """

##-------------------Start-of-__init__()-------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer_main:str, incoming_testing_material_answer_main_all:typing.List[str], incoming_incorrect_count:int, incoming_correct_count:int) -> None:

        """
        
        Initializes the word class\n

        Parameters:\n
        self (object - word) : the object being initialized\n
        incoming_id (int) : the id of the word\n
        incoming_testing_material (str) : the testing material of the word\n
        incoming_testing_material_pronunciation (str) : the pronunciation of the testing material of the word\n
        incoming_testing_material_answer (str) : the answer of the testing material of the word\n
        incoming_incorrect_count (int) : the number of incorrect guesses of the word\n
        incoming_correct_count (int) : the number of correct guesses of the word\n

        Returns:\n
        self (object - word) : the object being initialized

        """

        ## the id of the word
        self.id = incoming_id

        ## the thing being tested
        self.testing_material = incoming_testing_material

        ## the answer to the testing_material
        self.testing_material_answer_main = incoming_testing_material_answer_main

        self.testing_material_answer_all = incoming_testing_material_answer_main_all
        self.testing_material_answer_all.append(self.testing_material_answer_main)

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count = incoming_correct_count

        ## the type of the word
        self.word_type = 2 ## is currently numerical, plan to change this later

        ## the likelihood of the word being selected for testing
        self.likelihood = 0.0

        ## the known typos of the word
        self.typos = []

        ## the know incorrect typos of the word
        self.incorrect_typos = []

##-------------------start-of-check_answers_kana()-------------------------------------------------

    def check_answers_kana(self, userGuess:str, prompt:str) -> tuple[bool | None, str]:  


        if(userGuess == 'q'): # if the user wants to quit the program do so
            exit()
        
        if(userGuess not in self.testing_material_answer_all and userGuess != 'z' and userGuess.strip() != ''): ## checks if userGuess is a typo
            userGuess = self.check_typo(userGuess, prompt)

        if(userGuess in self.testing_material_answer_all): 
            return True, userGuess
        
        elif(userGuess != 'z'): 
            return False, userGuess
        
        else: ## z indicates the user is skipping the word
            return None, userGuess
        


#--------------------Start-of-check_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_typo(self, userGuess, prompt) -> str:  

        """

        checks if a userGuess is a typo or not

        Parameters:
        userGuess (string) a user's guess
        correctList (list - strings) a list of correct answers
        connection (object - mysql.connector.connect) a database connection object
        word_id (int) the id of the word the user is trying to guess

        Returns:
        final_answer (string) the user's final answer after being corrected for typos

        """

        minDistance = 3
        final_answer = userGuess

    
        if(userGuess in self.typos):
            return [item for item in self.typos if item == userGuess][0]
        ##elif(userGuess in itypos):
        ##    return userGuess

        for correct_answer in self.testing_material_answer_all:

            distance = util.levenshtein(userGuess, correct_answer)

            if(distance < minDistance):

                print("\nDid you mean : " + correct_answer + "? Press 1 to Confirm or 2 to Decline.\n")
            
                userA = int(util.input_check(1 ,str(msvcrt.getch().decode()), 2, prompt + "\nDid you mean : " + correct_answer + "? Press 1 to Confirm or 2 to Decline.\n"))
            
                util.clear_console()

                if(userA == 1):

                    final_answer = correct_answer

                  ##  add_Typo(userGuess,word_id,connection)

                    return final_answer

        ##add_Itypo(userGuess,word_id,connection)
        
        return final_answer
