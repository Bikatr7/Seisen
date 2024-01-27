class Entity:

    """
    
    Base class for all entities in Seisen.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,
                 id:int) -> None:
        
        """

        Initializes a new Entity object.

        Parameters:
        id (int) : The ID of the Entity.

        """

        self.id:int = id