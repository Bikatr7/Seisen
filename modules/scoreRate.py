## built-in modules
import random
import typing

## custom modules
from modules.words import word
from modules.dataHandler import dataHandler
from modules import util

class scoreRate:

    """
    
    The scoreRate class is used to determine which "word" will be given to the user based on a multitude of factors, such as number of answers, the number of correct answers, the number of incorrect answers etc.

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, handler:dataHandler):
        
        self.handler = handler


    def get_kana_to_test(self, kana_list:typing.List[word]):
        
        raw_score_list = []
        kana_scores = []
        display_item_list = []

        current_value = 0
        random_value = 0
        selection_range = 0
        default_score = 0
        i = 0

        for kana in kana_list:
            total_answer = kana.incorrect_count + kana.correct_count

            raw_score_list.append(kana.correct_count - kana.incorrect_count)
        
        default_score = max(abs(int(x)) for x in raw_score_list) + 1

        for raw_score in raw_score_list:
            kana_score = default_score

            if(raw_score > 0):
                kana_score -= raw_score

            elif(raw_score < 0):
                kana_score += abs(raw_score) 

            kana_scores.append(kana_score)
            selection_range += kana_score

        random_value = random.randint(1, selection_range)

        while(i < len(kana_scores) and current_value < random_value):
            current_value += kana_scores[i]
            i += 1

        kana_to_test = kana_list[i - 1]

        i = 0 

        while i < len(kana_list):

            kana_list[i].likelihood = round(((kana_scores[i-1] / selection_range) * 100),4)

            display_item_list.append(str(kana_list[i].likelihood) + "%")

            displayItem = "\n---------------------------------\nLikelihood : " + display_item_list[i] +"\njValue : " + kana_list[i].testing_material  + "\nP : " + str(kana_list[i].incorrect_count) + "\nC : " + str(kana_list[i].correct_count)  + "\nID : " + str(kana_list[i].id)  + "\n---------------------------------"
            
            display_item_list[-1] = displayItem

            i+=1

        display_item_list.sort()

        display_item_list = list(map(lambda x: str(display_item_list.index(x) + 1) + " " + str(x), display_item_list)) 

        return kana_to_test, display_item_list