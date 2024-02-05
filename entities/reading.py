## custom modules
from entities.entity import Entity

class Reading(Entity):

    """
    
    The Reading Class represents how a Word can be read.

    Contains both the furigana and the romaji.

    All Readings have a furigana, but if furigana is the same as the TestingMaterial, it can be assumed that that it is not a Kanji.
    
    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                word_id:int,
                id:int,
                furigana:str,
                romaji:str) -> None:
        
        """

        Initializes a new Reading object.

        Parameters:
        word_id (int) : The ID of the Word the Reading is for.
        id (int) : The ID of the Reading.
        furigana (str) : The furigana of the Reading.
        romaji (str) : The romaji of the Reading.

        """

        super().__init__(id)

        self.word_id:int = word_id

        self.furigana:str = furigana

        self.romaji:str = romaji