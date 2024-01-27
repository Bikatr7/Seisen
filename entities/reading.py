class Reading:

    """
    
    The Reading Class represents how a Word can be read.

    Contains both the furigana and the romaji.

    All Readings have a furigana, but if furigana is the same as the TestingMaterial, it can be assumed that that it is not a Kanji and should not be displayed.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                incoming_word_id:int,
                incoming_reading_id:int,
                incoming_furigana_value:str,
                incoming_romaji_value:str) -> None:
        
        """

        Initializes a new Reading object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the Reading is for.
        incoming_reading_id (int) : The ID of the Reading itself.
        incoming_furigana_value (str) : The value of the Reading's furigana.
        incoming_romaji_value (str) : The value of the Reading's romaji.

        """

        self.word_id:int = incoming_word_id

        self.reading_id:int = incoming_reading_id

        ## alias for reading_id, need to make this permanent later
        self.id = self.reading_id
        
        self.furigana_value:str = incoming_furigana_value

        self.romaji_value:str = incoming_romaji_value