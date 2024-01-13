

class TestingMaterial:

    """
    
    The TestingMaterial class represents the testing material of a Word and Vocab.

    Typically will be kanji, but in the case of Words or Vocab with no Kanji, it will be kana.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                incoming_word_id:int,
                incoming_testing_material_id:int,
                incoming_testing_material_value:str) -> None:
        
        """

        Initializes a new TestingMaterial object.

        Parameters:
        incoming_word_id (int) : The ID of the Word the TestingMaterial is for.
        incoming_testing_material_id (int) : The ID of the TestingMaterial itself.
        incoming_testing_material_value (str) : The value of the TestingMaterial.

        """

        self.word_id:int = incoming_word_id
        self.testing_material_id:int = incoming_testing_material_id
        self.testing_material_value:str = incoming_testing_material_value
