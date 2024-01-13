

class Furigana:

    """
    
    The Furigana class represents the furigana of a Word.

    Furigana is the Japanese reading aid for kanji. (Kana typically written above kanji.)

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                incoming_word_id:int,
                incoming_furigana_id:int,
                incoming_furigana_value:str) -> None:
        
        """

        Initializes a new Furigana object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the Furigana is for.
        incoming_furigana_id (int) : The ID of the Furigana itself.
        incoming_furigana_value (str) : The value of the Furigana.

        """

        self.word_id:int = incoming_word_id

        self.furigana_id:int = incoming_furigana_id
        
        self.furigana_value:str = incoming_furigana_value