## custom modules
from entities.entity import Entity

class TestingMaterial(Entity):

    """
    
    The TestingMaterial class represents the testing material of a Word.

    Typically will be kanji, but in the case of Words or Vocab with no Kanji, it will be kana.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                word_id:int,
                id:int,
                value:str) -> None:
        
        """

        Initializes a new TestingMaterial object.

        Parameters:
        word_id (int) : The ID of the Word the TestingMaterial is for.
        id (int) : The ID of the TestingMaterial.
        value (str) : The value of the TestingMaterial.

        """

        super().__init__(id)

        self.word_id:int = word_id

        self.value:str = value