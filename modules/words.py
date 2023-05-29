
class word():

    """
    
    The Superclass of all words in Seisen, all testing material in Seisen is part of or inherits this class
    
    """

##-------------------Start-of-__init__()-------------------------------------------------

    def __init__(self) -> None:

        """
        
        Initializes the word class\n

        Parameters:\n
        self (object - word) : the object being initialized\n

        Returns:\n
        None\n

        """

        ## the thing being tested
        self.testing_material = ""

        ## the answer to the testing_material
        self.testing_material_answer = ""

        ## the number of times the user answer to testing_material was incorrect
        self.incorrect_count = 0 

        ## the number of times the user answer to testing_material was correct
        self.correct_count = 0

        ## the prompt given to the user for the testing_material
        self.prompt = "What does " + self.testing_material + " mean?\n"