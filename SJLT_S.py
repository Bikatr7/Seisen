import pyautogui as gui # imports
import keyboard as key
import random as r 
import os
import sys

sys.path.insert(0, os.getcwd())

from SMFVF_S import *
from time import sleep

#--------------------Start-of-levenshtein()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def levenshtein(s1, s2): ## compares stringies

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

#--------------------Start-of-checkTypo()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def checkTypo(userGuess,correctList,connection,word_id): 

    minDistance = 3.25
    bestMatch = None
    newUserGuess = userGuess

    typos, itypos = readMultiColumnQuery(connection, 'select typos.typo,itypos.itypo from typos join itypos on typos.word_id = itypos.word_id where typos.word_id = ' + word_id)

    ##typos = readSingleColumnQuery(connection, 'select typo from typos where word_id = ' + word_id)
    ##itypos = readSingleColumnQuery(connection, 'select itypo from itypos where word_id = ' + word_id)

    if(userGuess in typos):
        return correctList[0]
    elif(userGuess in itypos):
        return userGuess

    for matchStr in correctList:
        distance = levenshtein(userGuess, matchStr)
        if(distance < minDistance):
            bestMatch = matchStr
          
    if(bestMatch != None):
        with open(r"C:\ProgramData\SJLT\prompt.txt", "r+",encoding="utf-8") as file:
            prompt = file.read()

        print("\nDid you mean : " + bestMatch + "? Press 1 to Confirm or 2 to Decline.\n")
        
        userA = int(inputCheck(1,key.read_key(),2,prompt + "\nDid you mean : " + bestMatch + "? Press 1 to Confirm or 2 to Decline.\n"))
        
        if(userA == 1):
            newUserGuess = bestMatch
            addtypo(userGuess,word_id,connection)
        else:
            additypo(userGuess,word_id,connection)

    os.system('cls')
    
    return newUserGuess

#--------------------Start-of-addTypo()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addtypo(typo,word_id,connection): 

    maxID = int(readSingleColumnQuery(connection,'select max(typo_id) from typos')[0]) + 1

    addToTypos(typo,word_id,maxID,connection)
    
#--------------------Start-of-addITypo()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def additypo(itypo,word_id,connection):

    maxID = int(readSingleColumnQuery(connection,'select max(itypo_id) from itypos')[0]) + 1

    addToItypos(itypo,word_id,maxID,connection)

#--------------------Start-of-checkAnswersEFB()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def checkAnswersEFB(userGuess,connection, word_id): 

    if(userGuess == 'q'):
        exit()

    clearStream()
    
    filteredEng = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + word_id)

    if(userGuess not in filteredEng):
        userGuess = checkTypo(userGuess,filteredEng,connection,word_id)

    if(userGuess in filteredEng): 
        return True,filteredEng,userGuess
    else:
        return False,filteredEng,userGuess
        
#--------------------Start-of-logProbChars()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logProbChars(connection,word_id): 

    currPValue = str(int(readSingleColumnQuery(connection,'select pValue from words where word_id = ' + word_id)[0]) + 1)

    executeQuery(connection,'update words set pValue = ' + currPValue + ' where word_id = ' + word_id)

#--------------------Start-of-logCorrChars()----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logCorrChars(connection,word_id):

    currCValue = str(int(readSingleColumnQuery(connection,'select cValue from words where word_id = ' + word_id)[0]) + 1)

    executeQuery(connection,'update words set cValue = ' + currCValue + ' where word_id = ' + word_id)

#----------------------------start-of-changeMode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def changeMode(): ## changes mode

    os.system('cls')

    print(mainMenu)

    sleep(0.17)

    newMode = int(inputCheck(1,key.read_key(),4,mainMenu))
    
    ecset(0,1,newMode,r"C:\ProgramData\SJLT\loopData.txt") ## changes mode in files

    if(modeNum != newMode and newMode == 1 or newMode == 2): ## if mode is for sjlt, generate a new schedule for that word bank
        sGenerateSchedule(connection,word_type=newMode)   
    elif(newMode == 3 and newMode != newMode):
        sGenerateSchedule(connection,word_type=0)   

    os.system('cls')

    return newMode
#---------------------start-of-sRate()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sRate(connection,word_type): 

    rawScoreValue,jValueScoreRateList = [],[]
    
    i,selectionRange,sRating,sRatingPrime = 0,0,0,0

    if(word_type == 0):
        corrCharCountList,probCharCountList,word_idList = readMultiColumnQuery(connection,'select cValue,pValue,word_id from words'+ '\norder by word_id asc;')
    else:
        corrCharCountList,probCharCountList,word_idList = readMultiColumnQuery(connection,'select cValue,pValue,word_id from words where word_type = ' + str(word_type) + '\norder by word_id asc;')

    while(i < len(corrCharCountList)): 
          rawScoreValue.append(int(corrCharCountList[i]) - int(probCharCountList[i]))
          i+=1
          
    sRatingPrime = max(abs(x) for x in rawScoreValue) + 2

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

#---------------------start-of-sGenerateSingle()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sGenerateSingle(connection,word_type):

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

        jVal,pVal,cVal = [result[0] for result in readMultiColumnQuery(connection, "select jValue,pValue,cValue from words where word_id = " + str(word_idList[i]))]

        display_score = str(round((score / selectionRange * 100), 4))

        displayList.append(display_score)

        display_item = "\n---------------------------------\nLikelyhood : " + display_score + "%  \njValue : " + jVal  + "\nP : " + pVal + "\nC : " + cVal  + "\nID : " + word_idList[i]  + "\n---------------------------------"
        
        displayList[-1] = display_item

    displayList.sort()

    displayList = list(map(lambda x: str(displayList.index(x) + 1) + " " + str(x), displayList)) 

    jVal,eVal = [result[0] for result in readMultiColumnQuery(connection,"select jValue,eValue from words where word_id = " + word_id)]

    return jVal,eVal,displayList,jValueScoreRateList,selectionRange,Chance,word_id 

 #---------------------start-of-sGenerateSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def sGenerateSchedule(connection, word_type):

    jValList, eValList, ChanceList, idList = [], [], [], []
    jValueScoreRateList, _, word_idList = sRate(connection, word_type)

    for i in range(4):
        jVal, eVal, _, jValueScoreRateList, _, Chance, word_id = sGenerateSingle(connection, word_type)
        jValList.append(jVal)
        eValList.append(eVal)
        ChanceList.append(Chance)
        idList.append(word_id)

    for i in range(3):

        max_index = jValueScoreRateList.index(max(jValueScoreRateList))

        idList.append(word_idList[max_index])

        jVal,eVal = [result[0] for result in readMultiColumnQuery(connection, "select jValue,eValue from words where word_id = " + str(word_idList[max_index]))]

        jValList.append(jVal)
        eValList.append(eVal)
        ChanceList.append("100%")

        jValueScoreRateList.pop(max_index)
        word_idList.pop(max_index)

    with open(r"C:\ProgramData\SJLT\sSchedule.txt", "w", encoding="utf-8") as schedule:
        for i in range(7):
            schedule.write(jValList[i] + "," + eValList[i] + "," + ChanceList[i] + "," + str(idList[i]) + ",\n")


#---------------------start-of-readSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def readSchedule(connection,word_type): 

    _,_,displayList,jValueScoreRateList,selectionRange,_,_ = sGenerateSingle(connection,word_type) 

    i,ii = 0,0
    buildStr = ""
    bleh = []

    if(os.stat(r"C:\ProgramData\SJLT\sSchedule.txt").st_size == 0): 
        sGenerateSchedule(connection,word_type)       
    
    with open(r"C:\ProgramData\SJLT\sSchedule.txt", "r+", encoding="utf-8") as ArrayRaw:
        Schedule = [x.strip() for x in ArrayRaw]
        
    currentLine = Schedule[0]

    count = currentLine.count(',') 

    while(i < count):
        if(currentLine[ii] != ","):
            buildStr += currentLine[ii]
        else:
            buildStr = buildStr.replace("'","")
            bleh.append(buildStr)
            buildStr = ""
            i+=1
        ii+=1

    return bleh[0],bleh[1],displayList,jValueScoreRateList,selectionRange,bleh[2],bleh[3] 

#---------------------start-of-updateSchedule()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def updateSchedule():

    with open(r"C:\ProgramData\SJLT\sSchedule.txt", "r+", encoding ="utf-8") as file:
        schedule = file.readlines()

    schedule.pop(0)

    if len(schedule) > 0:
        r.shuffle(schedule)

        schedule[len(schedule)-1] = schedule[len(schedule)-1].replace("\n","")

        with open(r"C:\ProgramData\SJLT\sSchedule.txt", "w+", encoding="utf-8") as file:
            file.writelines(schedule)
    else:
        with open(r"C:\ProgramData\SJLT\sSchedule.txt", "w", encoding="utf-8"):
            pass

#----------------------------------------------Start-of-SJLT()---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def SJLT(connection,word_type): 

        clearStream()

        os.system('cls')
        
        testJapanese,matchingEng,_,_,_,Chance,word_id = readSchedule(connection,word_type) 

        acceptedEngValues = []
        i = 0
        isCorrect,displayOther = True,False

        outputMsg = ""
        
        roundCount = int(readLoopData(2))
        numCorrect = int(readLoopData(3))

        fValue = readSingleColumnQuery(connection,'select fValue from words where word_id= ' + word_id)[0]

        ratio = roundCount and str(round(numCorrect / roundCount,2)) or str(0.0) 

        if(fValue != "None"): 
            testJapanese += "/" + fValue

        outputMsg = "You currently have " + str(numCorrect) + " out of " + str(roundCount) + " correct; Ratio : " + ratio + "\n"
        outputMsg += "Likelyhood : " + Chance
        outputMsg +=  "\n" + "-" * len(outputMsg)
        outputMsg += "\nWhat does " + testJapanese + " mean?\n"

        userGuess = str(input(outputMsg)).lower()

        with open(r"C:\ProgramData\SJLT\prompt.txt", "w+", encoding="utf-8") as file:
            file.write(outputMsg)


        if(userGuess == "v"): 
            changeMode()
        else:

            roundCount+=1
            isCorrect,acceptedEngValues,userGuess = checkAnswersEFB(userGuess,connection,word_id)

            os.system('cls')

            ##print("")

            if(isCorrect == True):
                numCorrect+=1
                outputMsg += "\n\nYou guessed " + userGuess + ", which is correct.\n"
                logCorrChars(connection,word_id)                

            else:
                outputMsg += "\n\nYou guessed " + userGuess + ", which is incorrect, the correct answer was " + matchingEng + ".\n"
                logProbChars(connection,word_id)
                                       

            while(i < len(acceptedEngValues)):

                if(isCorrect == False and matchingEng != userGuess):

                    if(displayOther == False):
                        outputMsg += "\nOther Answers include:\n"

                    outputMsg +=  "----------\n" + acceptedEngValues[i] + "\n"
                    displayOther = True

                elif(isCorrect == True and acceptedEngValues[i] != userGuess):

                    if(displayOther == False):
                        outputMsg += "\nOther Answers include:\n"
                        
                    outputMsg +=  "----------\n" + acceptedEngValues[i] + "\n"
                    displayOther = True
                i+=1
                        
            print(outputMsg)

            sleep(2)
                
            os.system('cls')

            updateSchedule()

        ecset(0,2,roundCount,r"C:\ProgramData\SJLT\loopData.txt")

        ecset(0,3,numCorrect,r"C:\ProgramData\SJLT\loopData.txt")

#-------------------Start-Of-saphTools()-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def saphTools(connection) : 

    outputMsg = "1.Print Character SRatings\n2.Query Nusevei\n3.Add To JSET\n4.Add To CSEP\n5.Search Term\n6.Replace Value\n7.Delete Value\n8.Refresh sSchedule"

    pathing,i = 0,0

    csepList = []

    clearStream()
    
    print(outputMsg)
    
    pathing = inputCheck(4,key.read_key(),8,outputMsg)
    
    clearStream()
    
    os.system('cls')

    if(pathing == "1"):
        
        _,_,sPrime,_,_,_,_ = sGenerateSingle(connection,word_type=0)
        
        while(i < len(sPrime)):
            print(sPrime[i] + " \n")
            i+=1
            
        os.system('pause')

    elif(pathing == "2"):
        
        query = input("Please enter query : \n")
        os.system('cls')

        try:
            print(readQueryRaw(connection,query))
            os.system('pause')
        except:
            print("Invalid Query\n")
            sleep(1)

    elif(pathing == "3"):

        new_word_id = int(readSingleColumnQuery(connection,'select max(word_id) from words')[0]) + 1
        new_csep_id = int(readSingleColumnQuery(connection,'select max(csep_id) from cseps')[0]) + 1
        
        word_type = 1

        inputForFur = None
        
        with open(r"kana.txt", "r+",encoding='utf-8') as ArrayRaw:
            kana = [x.strip() for x in ArrayRaw]

        try:
            inputForJap = userConfirm("Please Enter A Japanese Word\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")
            inputForJapRoma = userConfirm("Please Enter " + inputForJap + "'s Roma\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")
            inputForEng = userConfirm("Please Enter " + inputForJap + "'s English\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")

            while(input("Enter 1 if " + inputForJap + " has any additonal CSEP\n") == "1"):
                clearStream()
                csepList.append(userConfirm("Please Enter " + inputForJap + "'s additonal CSEP\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry"))

            while(i < len(inputForJap)):
                if(inputForJap[i] not in kana):
                    print("\n" + inputForJap[i] + " is kanji")
                    sleep(0.5)
                    inputForFur = userConfirm("Please Enter " + inputForJap + "'s Furigana\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")
                    break
                i+=1

            if(inputForFur == None):
                query = 'select word_id from words where jValue = "' + inputForJap + '" and jrValue = "' + inputForJapRoma + '" and fValue is Null'
            else:
                query = 'select word_id from words where jValue = "' + inputForJap + '" and jrValue = "' + inputForJapRoma + '" and fValue = "' + inputForFur + '"'

            word_id = readSingleColumnQuery(connection,query)

            if(len(word_id) == 0):
                addToJSET(inputForJap,inputForJapRoma,inputForEng,inputForFur,0,0,new_word_id,word_type,connection)
                addToCSEP(inputForEng,new_word_id,new_csep_id,connection)

                i = 0
                while(i < len(csepList)):
                    new_csep_id = int(readSingleColumnQuery(connection,'select max(csep_id) from cseps')[0]) + 1
                    addToCSEP(csepList[i],new_word_id,new_csep_id,connection)
                    i+=1
            else:
                print("This value is already in Nusevei : " + inputForJap + "\n")
                os.system('pause')

        except AssertionError:
            pass
            
    elif(pathing == "4"):
        
        word_id = userConfirm("Please Enter The ID Of The Word Where You Want To Add A CSEP To\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")
        jap = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + word_id)[0]

        if(len(jap) != 0):

            while(input("Enter 1 if " + jap + " has any additonal CSEP\n") == "1"):
                clearStream()
                inputForCsep  = userConfirm("Please Enter " + jap + "'s additonal CSEP\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")
                new_csep_id = int(readSingleColumnQuery(connection,'select max(csep_id) from cseps')[0]) + 1
                addToCSEP(inputForCsep,word_id,new_csep_id,connection)

        else:
            print(jap + " is not in Nusevei\n")
            os.system('pause')
        
    elif(pathing == "5"):

        term = input("Please select the term you are querying\n")

        os.system('cls')

        search(term,connection,None,1)

    elif(pathing =="6"):

        target_id = input("Please enter the id of the word/csep/typo/itypo you would like to replace\n")

        word = readSingleColumnQuery(connection,'select word_id from words where word_id = "' + target_id + '"')
        csep = readSingleColumnQuery(connection,'select csep_id from cseps where csep_id = "' + target_id + '"')
        itypo = readSingleColumnQuery(connection,'select itypo_id from itypos where itypo_id = "' + target_id + '"')
        typo = readSingleColumnQuery(connection,'select typo_id from typos where typo_id = "' + target_id + '"')

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

        clearStream()
        os.system('cls')

        replaceValue(typeReplacement,connection,target_id)

    elif(pathing == "7"):

        target_id = input("Please enter the id of the word/csep/typo/itypo you would like to delete\n")

        deleteValue(connection,target_id)

    elif(pathing == "8"):
        sGenerateSchedule(connection,word_type=0)
        
    else:
        ecset(0,1,-1,r"C:\ProgramData\SJLT\loopData.txt")

    os.system('cls')

#-------------------start of bootup()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bootup():

    print("Initalizing SJLT")
    
    exec(open(r"ensurefilesec.py", errors='ignore').read())

    os.system("title " + "SJLT Client")

    ecset(0,1,-1,r"C:\ProgramData\SJLT\loopData.txt")
    
    sleep(0.17)
    
    try:
        gui.getWindowsWithTitle("SJLT Client")[0].maximize()
    except:
        pass

    os.system('cls')
    
    print("SJLT Sucessfully Booted")

#-------------------start of initalizeConnection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def initalizeConnection():
        
        try:
                with open(r'C:\ProgramData\SJLT\pass.txt', 'r', encoding='utf-8') as file:  ## get saved connection key if exists
                    Pass = file.read()

                connection = createConnection("localhost","root",Pass,"nusevei")

                print("Used saved pass in C:\ProgramData\SJLT\pass.txt")

        except: ## else try to get pass manually
                Pass = input("Please enter the root password for your local database you have \n")

                try: ## if valid save the api key

                        connection = createConnection("localhost","root",Pass,"nusevei")
                            
                        if(os.path.exists(r'C:\ProgramData\SJLT\pass.txt') == False):
                            print("'C:\ProgramData\SJLT\pass.txt' was created due to lack of the file")
                            with open(r"C:\ProgramData\SJLT\pass.txt", "r+",encoding='utf-8') as file:
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
connection = initalizeConnection()

bootup()

valid_modes = [1,2,3,4]
mainMenu = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.J-E\n2.Kana Practice\n3.SJLT\n4.SAPH"

while True:
    modeNum = readLoopData(1)
    
    if(modeNum == 1):
        SJLT(connection,word_type=1)
    elif(modeNum == 2):
        SJLT(connection,word_type=2)
    elif(modeNum == 3):
        SJLT(connection,word_type=0)
    elif(modeNum == 4):
        saphTools(connection)
    elif(modeNum != -1):
        os.system('cls')
        print("Invalid Input, please enter a valid number choice or command.\n")

    if(modeNum not in valid_modes):
        modeNum = changeMode()
