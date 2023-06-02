class word:

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class

    Kana also uses this class.
    
    """

##-------------------Start-of-__init__()-------------------------------------------------

    def __init__(self, incoming_id:int, incoming_testing_material:str, incoming_testing_material_answer:str, incoming_incorrect_count:int, incoming_correct_count:int) -> None:

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
        self.testing_material_answer = incoming_testing_material_answer

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count = incoming_incorrect_count

        ## the number of times the user answer to testing_material was correct
        self.correct_count = incoming_correct_count

        ## the type of the word
        self.word_type = 2 ## is currently numerical, plan to change this later