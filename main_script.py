import pyautogui as gui # imports
import keyboard as key
import random as r 
import os
import ctypes

from associated_functions import core
from time import sleep

#--------------------Start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def levenshtein(s1, s2):

    """

    Compares two strings for similarity 

    Parameters:
    s1 (string)
    s2 (string)

    Returns:
    distance[sLength1][sLength2] (int) the minimum number of single-character edits required to transform s1 into s2

    """

    sLength1, sLength2 = len(s1), len(s2)
    distance = [[0] * (sLength2 + 1) for _ in range(sLength1 + 1)]
    
    for i in range(sLength1 + 1):
        distance[i][0] = i

    for ii in range(sLength2 + 1):
        distance[0][ii] = ii

    for i in range(1, sLength1 + 1):
        for ii in range(1, sLength2 + 1):

            if(s1[i - 1] == s2[ii - 1]):
                cost = 0
            else:
                cost = 1

            distance[i][ii] = min(distance[i - 1][ii] + 1, distance[i][ii- 1] + 1, distance[i - 1][ii - 1] + cost)

            if(i > 1 and ii > 1 and s1[i-1] == s2[ii-2] and s1[i-2] == s2[ii-1]):
                distance[i][ii] = min(distance[i][ii], distance[i-2][ii-2] + cost)

    return distance[sLength1][sLength2]

#--------------------Start-of-check_typo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_typo(userGuess,correctList,connection,word_id): 

    """

    checks if a userGuess is a typo or not

    Parameters:
    userGuess (string) a user's guess
    correctList (list - strings) a list of correct answers
    connection (object - mysql.connector.connect) a database connection object
    word_id (int) the id of the word the user is trying to guess

    Returns:
    finalAnswer (string) the user's final answer after being corrected for typos

    """

    minDistance = 3
    finalAnswer = userGuess

    typos, itypos = core.read_multi_column_query(connection, 'select typos.typo,itypos.itypo from typos join itypos on typos.word_id = itypos.word_id where typos.word_id = ' + word_id)

    if(userGuess in typos):
        return correctList[0]
    elif(userGuess in itypos):
        return userGuess

    for correctAnswer in correctList:

        distance = levenshtein(userGuess, correctAnswer)

        if(distance < minDistance):

            with open(r"C:\ProgramData\SJLT\prompt.txt", "r+",encoding="utf-8") as file:
                prompt = file.read()

            print("\nDid you mean : " + correctAnswer + "? Press 1 to Confirm or 2 to Decline.\n")
        
            userA = int(core.input_check(1,key.read_key(),2,prompt + "\nDid you mean : " + correctAnswer + "? Press 1 to Confirm or 2 to Decline.\n"))
        
            os.system('cls')

            if(userA == 1):

                finalAnswer = correctAnswer

                add_Typo(userGuess,word_id,connection)

                return finalAnswer

    add_Itypo(userGuess,word_id,connection)
    
    return finalAnswer

#--------------------Start-of-add_Typo()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_Typo(typo,word_id,connection): 

    """

    adds a typo to the database

    Parameters:
    typo (string) a typo
    word_id (int) the id of the word the user is trying to guess
    connection (object - mysql.connector.connect) a database connection object

    Returns:
    None

    """

    typo_idList = core.read_single_column_query(connection,'select typo_id from typos'+ '\norder by typo_id asc;')

    core.add_to_Typos(typo,word_id,core.get_new_id(typo_idList),connection)
    
#--------------------Start-of-add_Itypo()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_Itypo(itypo,word_id,connection):

    """

    adds an itypo to the database

    Parameters:
    itypo (string) an itypo
    word_id (int) the id of the word the user is trying to guess
    connection (object - mysql.connector.connect) a database connection object

    Returns:
    None

    """

    itypo_idList = core.read_single_column_query(connection,'select itypo_id from itypos'+ '\norder by itypo_id asc;')

    core.add_to_Itypos(itypo,word_id,core.get_new_id(itypo_idList),connection)
    
#--------------------Start-of-log_prob_chars()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def log_prob_chars(connection,word_id): 

    """

    updates a word's pValue

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_id (int) the id of the word the user is trying to guess

    Returns:
    None

    """

    currPValue = str(int(core.read_single_column_query(connection,'select pValue from words where word_id = ' + word_id)[0]) + 1)

    core.execute_query(connection,'update words set pValue = ' + currPValue + ' where word_id = ' + word_id)

#--------------------Start-of-log_corr_chars()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def log_corr_chars(connection,word_id):

    """

    updates a word's cValue

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_id (int) the id of the word the user is trying to guess

    Returns:
    None

    """

    currCValue = str(int(core.read_single_column_query(connection,'select cValue from words where word_id = ' + word_id)[0]) + 1)

    core.execute_query(connection,'update words set cValue = ' + currCValue + ' where word_id = ' + word_id)

#----------------------------start-of-change_mode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def change_mode(): ## changes mode

    """

    changes Seisen's active mode

    Parameters:
    None

    Returns:
    newMode (int) the new mode for Seisen

    """

    os.system('cls')

    print(mainMenu)

    newMode = int(core.input_check(1,key.read_key(),3,mainMenu))
    
    core.ecset(0,1,newMode,r"C:\\ProgramData\\SJLT\\loopData.txt") ## changes mode in files

    if(modeNum != newMode and (newMode == 1 or newMode == 2)): ## mode 1 and mode 2 have their word type match their modes
        generate_sSchedule(connection,word_type=newMode)   
    elif(modeNum != newMode and (newMode == 3)): ## mode 3 does not have a word type
        pass

    os.system('cls')

    return newMode

#---------------------start-of-sRate()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sRate(connection,word_type): 

    """

    'sRates' the words for word_type word_type

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (int) the type of word we are 'sRating'

    Returns:
    jValueScoreRateList (list - int) the base rating for selection, the higher the value, the more likely the word will be selected
    selectionRange (int) the range for selection, all the jValueScoreRateList elements added together
    word_idList (list - string) a list of all the id's for word_type 'word_type'

    """

    rawScoreValue,jValueScoreRateList = [],[]
    
    i,selectionRange,sRating,sRatingPrime = 0,0,0,0

    if(word_type == 0):
        corrCharCountList,probCharCountList,word_idList = core.read_multi_column_query(connection,'select cValue,pValue,word_id from words'+ '\norder by word_id asc;')
    else:
        corrCharCountList,probCharCountList,word_idList = core.read_multi_column_query(connection,'select cValue,pValue,word_id from words where word_type = ' + str(word_type) + '\norder by word_id asc;')

    while(i < len(corrCharCountList)): 
          rawScoreValue.append(int(corrCharCountList[i]) - int(probCharCountList[i]))
          i+=1
          
    sRatingPrime = max(abs(int(x)) for x in rawScoreValue) + 2

    i = 0
    
    while(i < len(rawScoreValue)):
        sRating = sRatingPrime
        if(rawScoreValue[i] > 0):  
            sRating -= rawScoreValue[i]
        elif(rawScoreValue[i] < 0):
            sRating += abs(rawScoreValue[i] * 10)

        jValueScoreRateList.append(sRating) 
        selectionRange += sRating 
        i+=1

    return jValueScoreRateList,selectionRange,word_idList

#---------------------start-of-generate_sSingle()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_sSingle(connection,word_type):

    """

    generates a single word based on it's sScore for Seisen testing

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (int) the type of word we are looking to generate

    Returns:
    jValue (string) the japanese value of the word generated
    eValue (string) the english value of the word generated
    jValueScoreRateList (list - int) the base rating for selection, the higher the value, the more likely the word will be selected
    selectionRange (int) the range for selection, all the jValueScoreRateList elements added together
    displayList (list - string) a display that is printed when looking at how sRate rates words
    chance (string) the likelihood of this specific word being generated
    word_id (string) the id of the word we generated

    """

    jValueScoreRateList,selectionRange,word_idList = sRate(connection,word_type) 
    
    ranVal = r.randint(1,selectionRange) 
    i,currVal = 0,0
    jVal,eVal,Chance= "","",""
    displayList = []

    while(i < len(jValueScoreRateList) and currVal < ranVal): 
        currVal += jValueScoreRateList[i]
        i+=1

    word_id = word_idList[i-1]

    Chance = str(round(((jValueScoreRateList[i-1] / selectionRange) * 100),4)) + "%"

    for i, score in enumerate(jValueScoreRateList):

        jVal,pVal,cVal = [result[0] for result in core.read_multi_column_query(connection, "select jValue,pValue,cValue from words where word_id = " + str(word_idList[i]))]

        displayScore = str(round((score / selectionRange * 100), 4))

        displayList.append(displayScore)

        displayItem = "\n---------------------------------\nLikelihood : " + displayScore + "%  \njValue : " + jVal  + "\nP : " + pVal + "\nC : " + cVal  + "\nID : " + word_idList[i]  + "\n---------------------------------"
        
        displayList[-1] = displayItem

    displayList.sort()

    displayList = list(map(lambda x: str(displayList.index(x) + 1) + " " + str(x), displayList)) 

    jVal,eVal = [result[0] for result in core.read_multi_column_query(connection,"select jValue,eValue from words where word_id = " + word_id)]

    return jVal,eVal,displayList,jValueScoreRateList,selectionRange,Chance,word_id 

 #---------------------start-of-generate_sSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def generate_sSchedule(connection, word_type):

    """

    generates a schedule for Seisen testing

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (int) the type of word we are looking to generate

    Returns:
    None

    """

    jValList, eValList, chanceList, idList = [], [], [], []
    jValueScoreRateList, _, word_idList = sRate(connection, word_type)

    for i in range(4):
        jVal, eVal, _, _, _, Chance, word_id = generate_sSingle(connection, word_type)
        jValList.append(jVal)
        eValList.append(eVal)
        chanceList.append(Chance)
        idList.append(word_id)

    maxIndex = jValueScoreRateList.index(max(jValueScoreRateList))

    for i in range(3):

        idList.append(word_idList[maxIndex])

        jVal,eVal = [result[0] for result in core.read_multi_column_query(connection, "select jValue,eValue from words where word_id = " + str(word_idList[maxIndex]))]

        jValList.append(jVal)
        eValList.append(eVal)
        chanceList.append("100%")

        jValueScoreRateList.pop(maxIndex)
        word_idList.pop(maxIndex)

    with open(r"C:\\ProgramData\\SJLT\\sSchedule.txt", "w", encoding="utf-8") as schedule:
        for i in range(7):
            schedule.write(jValList[i] + "," + eValList[i] + "," + chanceList[i] + "," + str(idList[i]) + ",\n")


#---------------------start-of-read_sSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_sSchedule(connection,word_type): 

    """

    reads the schedule for Seisen testing

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (int) the type of word we are looking to generate

    Returns:
    jValue (string) the japanese value of the word being read
    eValue (string) the english value of the word being read
    displayList (list - string) a display that is printed when looking at how sRate rates words
    jValueScoreRateList (list - int) the base rating for selection, the higher the value, the more likely the word will be selected
    selectionRange (int) the range for selection, all the jValueScoreRateList elements added together
    word_id (string) the id of the word being read

    """

    _,_,displayList,jValueScoreRateList,selectionRange,_,_ = generate_sSingle(connection,word_type) 

    i,ii = 0,0
    buildStr = ""
    schedulePart = []

    if(os.stat(r"C:\\ProgramData\\SJLT\\sSchedule.txt").st_size == 0): 
        generate_sSchedule(connection,word_type)       
    
    with open(r"C:\\ProgramData\\SJLT\\sSchedule.txt", "r+", encoding="utf-8") as ArrayRaw:
        schedule = [x.strip() for x in ArrayRaw]
        
    currentLine = schedule[0]

    count = currentLine.count(',') 

    while(i < count):
        if(currentLine[ii] != ","):
            buildStr += currentLine[ii]
        else:
            buildStr = buildStr.replace("'","")
            schedulePart.append(buildStr)
            buildStr = ""
            i+=1
        ii+=1

    jValue = schedulePart[0]
    eValue = schedulePart[1]
    chance = schedulePart[2]
    word_id = schedulePart[3]
    
    return jValue,eValue,displayList,jValueScoreRateList,selectionRange,chance,word_id

#---------------------start-of-update_sSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_sSchedule():

    """

    updates the Seisen schedule

    Parameters:
    None

    Returns:
    None

    """

    with open(r"C:\ProgramData\SJLT\sSchedule.txt", "r+", encoding ="utf-8") as file:
        schedule = file.readlines()

    schedule.pop(0)

    if(len(schedule) > 0):
        r.shuffle(schedule)

        schedule[len(schedule)-1] = schedule[len(schedule)-1].replace("\n","")

        with open(r"C:\ProgramData\SJLT\sSchedule.txt", "w+", encoding="utf-8") as file:
            file.writelines(schedule)
    else:
        with open(r"C:\ProgramData\SJLT\sSchedule.txt", "w", encoding="utf-8"):
            pass

#--------------------Start-of-check_answers_EFB()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_answers_EFB(userGuess,connection,word_id): 

    """

    checks if the user guess is correct for english-fill-blank

    Parameters:
    userGuess (string) the user's guess
    connection (object - mysql.connector.connect) a database connection object
    word_id (string) the id of the word being guessed

    Returns:
    'result' (boolean) True if the user's guess is correct, False if the user's guess is incorrect, None if the user wants to skip the word
    filteredEng (list - string) the correct english values for the word
    userGuess (string) the user's guess

    """

    if(userGuess == 'q'): # if the user wants to quit the program do so
        exit()

    core.clear_stream()
    
    filteredEng = core.read_single_column_query(connection,'select csep from cseps where word_id = ' + word_id) # gets the correct english values for the word

    if(userGuess not in filteredEng and userGuess != 'z' and userGuess.strip() != ''): ## checks if userGuess is a typo
        userGuess = check_typo(userGuess,filteredEng,connection,word_id)

    if(userGuess in filteredEng): 
        return True,filteredEng,userGuess
    
    elif(userGuess != 'z'): 
        return False,filteredEng,userGuess
    
    else: ## z indicates the user is skipping the word
        return None,filteredEng,userGuess

#--------------------Start-of-check_answers_RFB()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_answers_RFB(userGuess,connection,word_id):

    """

    checks if the user guess is correct for romaji-fill-blank

    Parameters:
    userGuess (string) the user's guess
    connection (object - mysql.connector.connect) a database connection object
    word_id (string) the id of the word being guessed

    Returns:
    'result' (boolean) True if the user's guess is correct, False if the user's guess is incorrect, None if the user wants to skip the word
    userGuess (string) the user's guess

    """

    if(userGuess == 'q'): ## if the user wants to quit the program do so
        exit()

    core.clear_stream()
    
    correctRoma = core.read_single_column_query(connection,'select jrValue from words where word_id = ' + word_id)

    if(userGuess not in correctRoma and userGuess != 'z' and userGuess.strip() != ''): ## checks if userGuess is a typo
        userGuess = check_typo(userGuess,correctRoma,connection,word_id)

    if(userGuess in correctRoma): 
        return True,userGuess
    
    elif(userGuess != 'z'): 
        return False,userGuess
    
    else: ## z indicates the user is skipping the word
        return None,userGuess
    
#----------------------------------------------Start-of-SJLT()---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def SJLT(connection,word_type): 

    """
    
    the main 'trainer' function for Seisen, it is used for kana testing and EFB (English-Fill-Blank) testing

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (string) the type of word being tested

    Returns:
    None

    """

    core.clear_stream()

    os.system('cls')
    
    testJapanese,matchingEng,_,_,_,Chance,word_id = read_sSchedule(connection,word_type) 

    acceptedEngValues = []
    i = 0
    isCorrect,displayOther = True,False

    outputMsg = ""
    
    roundCount = int(core.read_loop_data(2))
    numCorrect = int(core.read_loop_data(3))

    fValue = core.read_single_column_query(connection,'select fValue from words where word_id = ' + word_id)[0]

    ratio = roundCount and str(round(numCorrect / roundCount,2)) or str(0.0) 

    outputMsg = "You currently have " + str(numCorrect) + " out of " + str(roundCount) + " correct; Ratio : " + ratio + "\n"
    outputMsg += "Likelihood : " + Chance
    outputMsg +=  "\n" + "-" * len(outputMsg)
    outputMsg += "\nWhat does " + testJapanese + " mean?\n"

    if(fValue != "None"): ## if the word has a furigana value add it to the output message
        testJapanese += "/" + fValue

    outputMsgRoma = "You currently have " + str(numCorrect) + " out of " + str(roundCount) + " correct; Ratio : " + ratio + "\n"
    outputMsgRoma += "Likelihood : " + Chance
    outputMsgRoma +=  "\n" + "-" * len(outputMsgRoma)
    outputMsgRoma += "\nWhat does " + testJapanese  + " mean?\n"

    userGuess = str(input(outputMsg)).lower()

    with open(r"C:\ProgramData\SJLT\prompt.txt", "w+", encoding="utf-8") as file:
        file.write(outputMsg)

    if(userGuess == "v"): ## if the user wants to change the mode do so
        change_mode()
        return
    
    elif(userGuess == "b"): ## if user wants to show the furigana do so

        os.system('cls')
        userGuess = str(input(outputMsgRoma)).lower()

        if(userGuess == "v"): ## if the user wants to change the mode do so
            change_mode()
            return

        with open(r"C:\ProgramData\SJLT\prompt.txt", "w+", encoding="utf-8") as file: ## stores prompt for later
            file.write(outputMsgRoma)

    roundCount+=1
    isCorrect,acceptedEngValues,userGuess = check_answers_EFB(userGuess,connection,word_id) ## checks if the user's guess is correct

    os.system('cls')

    if(isCorrect == True):
        numCorrect+=1
        outputMsgRoma += "\n\nYou guessed " + userGuess + ", which is correct.\n"
        log_corr_chars(connection,word_id)                

    elif(isCorrect == False):
        outputMsgRoma += "\n\nYou guessed " + userGuess + ", which is incorrect, the correct answer was " + matchingEng + ".\n"
        log_prob_chars(connection,word_id)

    else:
        outputMsgRoma += "\n\nSkipped.\n"
        log_prob_chars(connection,word_id) 

    while(i < len(acceptedEngValues)): ## displays other possible answers

        if(isCorrect == None or isCorrect == False and matchingEng != userGuess):

            if(displayOther == False):
                outputMsgRoma += "\nOther Answers include:\n"

            outputMsgRoma +=  "----------\n" + acceptedEngValues[i] + "\n"
            displayOther = True

        elif(isCorrect == True and acceptedEngValues[i] != userGuess):

            if(displayOther == False):
                outputMsgRoma += "\nOther Answers include:\n"
                
            outputMsgRoma +=  "----------\n" + acceptedEngValues[i] + "\n"
            displayOther = True

        i+=1
                
    print(outputMsgRoma)

    sleep(2)
        
    os.system('cls')

    update_sSchedule()

    core.ecset(0,2,roundCount,r"C:\ProgramData\SJLT\loopData.txt") ## updates the loop data for number of rounds

    core.ecset(0,3,numCorrect,r"C:\ProgramData\SJLT\loopData.txt") ## updates the loop data for number of correct answers
 
#----------------------------------------------Start-of-SJLT_Romaji()---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def SJLT_Romaji(connection,word_type): 
        
    """
    
    a secondary 'trainer' function for Seisen, it is used for romaji testing

    Parameters:
    connection (object - mysql.connector.connect) a database connection object
    word_type (string) the type of word being tested

    Returns:
    None

    """

    core.clear_stream()

    os.system('cls')
    
    testJapanese,matchingEng,_,_,_,Chance,word_id = read_sSchedule(connection,word_type) 

    isCorrect = True

    outputMsg = ""
    
    roundCount = int(core.read_loop_data(2))
    numCorrect = int(core.read_loop_data(3))

    correctRoma = core.read_single_column_query(connection,'select jrValue from words where word_id = ' + word_id)[0]

    ratio = roundCount and str(round(numCorrect / roundCount,2)) or str(0.0) 

    outputMsg = "You currently have " + str(numCorrect) + " out of " + str(roundCount) + " correct; Ratio : " + ratio + "\n"
    outputMsg += "Likelihood : " + Chance
    outputMsg +=  "\n" + "-" * len(outputMsg)
    outputMsg += "\nHow do you pronounce " + testJapanese + "?\n"

    testJapanese += "/" + matchingEng ## adds the matching english value to the output message if it exists

    outputMsgRoma = "You currently have " + str(numCorrect) + " out of " + str(roundCount) + " correct; Ratio : " + ratio + "\n"
    outputMsgRoma += "Likelihood : " + Chance
    outputMsgRoma +=  "\n" + "-" * len(outputMsgRoma)
    outputMsgRoma += "\nHow do you pronounce " + testJapanese + "?\n"

    userGuess = str(input(outputMsg)).lower()

    with open(r"C:\ProgramData\SJLT\prompt.txt", "w+", encoding="utf-8") as file: ## stores prompt for later
        file.write(outputMsg)

    if(userGuess == "v"): ## if the user wants to change the mode do so
        change_mode()
        return
    
    elif(userGuess == "b"): ## if user wants to show the english value do so

        os.system('cls')
        userGuess = str(input(outputMsgRoma)).lower()

        if(userGuess == "v"): 
            change_mode()
            return

        with open(r"C:\ProgramData\SJLT\prompt.txt", "w+", encoding="utf-8") as file:
            file.write(outputMsgRoma)

    roundCount+=1
    isCorrect,userGuess = check_answers_RFB(userGuess,connection,word_id) ## checks if the user's guess is correct

    os.system('cls')

    if(isCorrect == True):
        numCorrect+=1
        outputMsgRoma += "\n\nYou guessed " + userGuess + ", which is correct.\n"
        log_corr_chars(connection,word_id)                

    elif(isCorrect == False):
        outputMsgRoma += "\n\nYou guessed " + userGuess + ", which is incorrect, the correct answer was " + correctRoma + ".\n"
        log_prob_chars(connection,word_id)

    else:
        outputMsgRoma += "\n\nSkipped.\n"
        log_prob_chars(connection,word_id) 
                
    print(outputMsgRoma)

    sleep(2)
        
    os.system('cls')

    update_sSchedule()

    core.ecset(0,2,roundCount,r"C:\ProgramData\SJLT\loopData.txt") ## updates the loop data for number of rounds

    core.ecset(0,3,numCorrect,r"C:\ProgramData\SJLT\loopData.txt") ## updates the loop data for number of correct answers

#-------------------Start-Of-SAPH_tools()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def SAPH_tools(connection) : 

    """
    
    a multi purpose function for Seisen, it is used for various tasks, mostly related to the database 

    Parameters:
    connection (object - mysql.connector.connect) a database connection object

    Returns:
    None

    """

    outputMsg = "1.Print Character SRatings\n2.Query Nusevei\n3.Add To JSET\n4.Add To CSEP\n5.Search Term\n6.Replace Value\n7.Delete Value\n8.Refresh sSchedule"

    pathing,i = 0,0

    csepList = []

    core.clear_stream()
    
    print(outputMsg)
    
    pathing = core.input_check(4,key.read_key(),8,outputMsg)
    
    core.clear_stream()
    
    os.system('cls')

    if(pathing == "1"): ## prints the SRatings of all characters
        
        _,_,sPrime,_,_,_,_ = generate_sSingle(connection,word_type=0)
        
        while(i < len(sPrime)):
            print(sPrime[i] + " \n")
            i+=1
            
        os.system('pause')

    elif(pathing == "2"): ## queries the Nusevei database
        
        query = input("Please enter query : \n")
        os.system('cls')

        try:
            print(core.read_raw_query(connection,query))
            os.system('pause')
        except:
            print("Invalid Query\n")
            sleep(1)

    elif(pathing == "3"): ## adds a value to words table

        new_word_id = core.get_new_id(core.read_single_column_query(connection,'select word_id from words'+ '\norder by word_id asc;'))
        new_csep_id = core.get_new_id(core.read_single_column_query(connection,'select csep_id from cseps'+ '\norder by csep_id asc;'))
        
        word_type = 1

        inputForFur = None
        
        with open(r"kana.txt", "r+",encoding='utf-8') as ArrayRaw: ## reads the kana.txt file for all kana
            kana = [x.strip() for x in ArrayRaw]

        try:
            inputForJap = core.user_confirm("Please Enter A Japanese Word\n")

            inputForJapRoma = core.user_confirm("Please Enter " + inputForJap + "'s Roma\n")
            inputForEng = core.user_confirm("Please Enter " + inputForJap + "'s English\n")

            while(input("Enter 1 if " + inputForJap + " has any additional CSEP\n") == "1"):
                core.clear_stream()
                csepList.append(core.user_confirm("Please Enter " + inputForJap + "'s additional CSEP\n"))

            while(i < len(inputForJap)):
                if(inputForJap[i] not in kana):
                    print("\n" + inputForJap[i] + " is kanji")
                    sleep(0.5)
                    inputForFur = core.user_confirm("Please Enter " + inputForJap + "'s Furigana\n")
                    break
                i+=1

            if(inputForFur == None):
                query = 'select word_id from words where jValue = "' + inputForJap + '" and jrValue = "' + inputForJapRoma + '" and fValue is Null'
            else:
                query = 'select word_id from words where jValue = "' + inputForJap + '" and jrValue = "' + inputForJapRoma + '" and fValue = "' + inputForFur + '"'

            word_id = core.read_single_column_query(connection,query)

            if(len(word_id) == 0):

                core.add_to_JSET(inputForJap,inputForJapRoma,inputForEng,inputForFur,0,0,new_word_id,word_type,connection)
                core.add_to_CSEP(inputForEng,new_word_id,new_csep_id,connection)

                i = 0
                while(i < len(csepList)):
                    
                    new_csep_id = core.get_new_id(core.read_single_column_query(connection,'select csep_id from cseps'+ '\norder by csep_id asc;'))
                    core.add_to_CSEP(csepList[i],new_word_id,new_csep_id,connection)
                    i+=1
            else:
                print("This value is already in Nusevei : " + inputForJap + "\n")
                os.system('pause')

        except AssertionError: ## if the user enters 'z', the program will return to the main menu as 'z' is the skip key
            pass
            
    elif(pathing == "4"): ## adds a value to cseps table

        try:
        
            word_id = core.user_confirm("Please Enter The ID Of The Word Where You Want To Add A CSEP To\n")

            if(word_id.isnumeric() == False):
                raise core.UnexpectedInputError

            jap = core.read_single_column_query(connection,'select jValue from words where word_id = ' + word_id)[0]

            if(len(jap) != 0):

                while(input("Enter 1 if " + jap + " has any additional CSEP\n") == "1"):

                    core.clear_stream()
                    inputForCsep  = core.user_confirm("Please Enter " + jap + "'s additional CSEP\n")
                    new_csep_id = core.get_new_id(core.read_single_column_query(connection,'select csep_id from cseps'+ '\norder by csep_id asc;'))
                    core.add_to_CSEP(inputForCsep,word_id,new_csep_id,connection)

            else:
                print(jap + " is not in Nusevei\n")
                os.system('pause')
        
        except AssertionError: ## if the user enters 'z', the program will return to the main menu as 'z' is the skip key
            pass

        except core.UnexpectedInputError:
            pass


    elif(pathing == "5"): ## searches the Nusevei Database

        term = input("Please select the term you are querying\n")

        os.system('cls')

        core.search(term,connection,None,1)
 
    elif(pathing == "6"): ## replaces a value in the database

        try:
            
            target_id = input("Please enter the id of the word/csep/typo/itypo you would like to replace\n")
            
            assert target_id != 'z'

            word = core.read_single_column_query(connection,'select word_id from words where word_id = "' + target_id + '"')
            csep = core.read_single_column_query(connection,'select csep_id from cseps where csep_id = "' + target_id + '"')
            itypo = core.read_single_column_query(connection,'select itypo_id from itypos where itypo_id = "' + target_id + '"')
            typo = core.read_single_column_query(connection,'select typo_id from typos where typo_id = "' + target_id + '"')

            print("\n")

            if(len(word) == 1):
                print("Nusevei has confirmed the existence of a word with an id of " + target_id + " \nPress 1 to edit this word\n")
            if(len(csep) == 1):
                print("Nusevei has confirmed the existence of a csep with an id of " + target_id + "\nPress 2 to edit this word\n")
            if(len(typo) == 1):
                print("Nusevei has confirmed the existence of a itypo with an id of " + target_id + "\nPress 3 to edit this word\n")
            if(len(itypo) == 1):
                print("Nusevei has confirmed the existence of a typo with an id of " + target_id + "\nPress 4 to edit this word\n")

            sleep(.7)

            typeReplacement = key.read_key() 

            core.clear_stream()
            os.system('cls')

            core.replace_value(typeReplacement,connection,target_id)

        except AssertionError:
            pass

    elif(pathing == "7"): ## deletes a value in the database

        target_id = input("Please enter the id of the word/csep/typo/itypo you would like to delete\n")

        core.delete_value(connection,target_id)

    elif(pathing == "8"): ## generates a new schedule
        generate_sSchedule(connection,word_type=0)
        
    else: ## returns to the main while loop
        core.ecset(0,1,-1,r"C:\ProgramData\SJLT\loopData.txt")

    os.system('cls')

#-------------------start of bootup()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bootup():

    """
    This function is called when the program is first run. It initializes the program and sets up the console window.

    Parameters:
    None

    Returns:
    None

    """

    print("Initializing Seisen")
    
    exec(open(r"ensure_file_sec.py", errors='ignore').read()) ## ensures that the program has the necessary files to run

    os.system("title " + "Seisen") ## sets the title of the console window

    core.ecset(0,1,-1,r"C:\ProgramData\SJLT\loopData.txt")
    
    sleep(0.1)
    
    hwnd = ctypes.windll.kernel32.GetConsoleWindow() ## sets the console window to fullscreen
    ctypes.windll.user32.ShowWindow(hwnd, 3) 

    os.system('cls')
    
    print("SJLT Successfully Booted")

#-------------------start of initialize_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def initialize_connection():

    """

    Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.

    Parameters:
    None

    Returns:
    connection (object - mysql.connector.connect) The connection to the database

    """
        
    try:

        with open(r'C:\ProgramData\SJLT\pass.txt', 'r', encoding='utf-8') as file:  ## get saved connection key if exists
            Pass = file.read()

        connection = core.create_connection("localhost","root",Pass,"nusevei")

        print("Used saved pass in C:\\ProgramData\\SJLT\\pass.txt")

    except: ## else try to get pass manually
            
        Pass = input("Please enter the root password for your local database you have\n")

        try: ## if valid save the api key

            connection = core.create_connection("localhost","root",Pass,"nusevei")
                        
            if(os.path.exists(r'C:\\ProgramData\\SJLT\\pass.txt') == False):
                print("'C:\\ProgramData\\SJLT\\pass.txt' was created due to lack of the file")
                with open(r"C:\\ProgramData\\SJLT\\pass.txt", "r+",encoding='utf-8') as file:
                    file.write(Pass)

            sleep(0.1)
                
        except Exception as e: ## if invalid exit
                    
            os.system('cls')

            print(str(e))
            print("Error with creating connection object, please double check your password\n")
            os.system('pause')
            
            exit()

    return connection
    
#-------------------start of main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

connection = initialize_connection()

bootup()

validModes = [1,2,3] ## -1 is meant to be a code that forces the input to be changed

mainMenu = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.J-E\n2.Kana Practice\n3.SAPH"

while True: ## main loop
    modeNum = core.read_loop_data(1)
    
    if(modeNum == 1):
        if(r.randint(1,2) == 1):
            SJLT(connection,word_type=1)
        else:
            SJLT_Romaji(connection,word_type=1)
    elif(modeNum == 2):
        SJLT(connection,word_type=2)
    elif(modeNum == 3):
        SAPH_tools(connection)
    elif(modeNum != -1): ## if invalid input, clear screen and print error
        os.system('cls')
        print("Invalid Input, please enter a valid number choice or command.\n")

    if(modeNum not in validModes): ## if invalid mode, change mode
        modeNum = change_mode()
