import os  
import keyboard as key
import msvcrt
import mysql.connector

from time import sleep

#-------------------Start-of-search()---------------------------------------------------------

def search(term,connection,force_return_value,pause_value):

    Jap = readSingleColumnQuery(connection,'select jValue from words where jValue = "' + term + '"')
    Jap_roma = readSingleColumnQuery(connection,'select jrValue from words where jrValue = "' + term + '"')
    Eng = readSingleColumnQuery(connection,'select eValue from words where eValue = "' + term + '"')
    Furi = readSingleColumnQuery(connection,'select fValue from words where fValue != 0 and fValue = "' + term + '"')
    corr = readSingleColumnQuery(connection,'select cValue from words where cValue = "' + term + '"')
    prob = readSingleColumnQuery(connection,'select pValue from words where pValue = "' + term + '"')
    csep_line = readSingleColumnQuery(connection,'select csep from cseps where csep_id = "' + term + '"')
    csep_actual = readSingleColumnQuery(connection,'select csep from cseps where csep = "' + term + '"')
    word_id = readSingleColumnQuery(connection,'select jValue from words where word_id = "' + term + '"')
    typo_actual = readSingleColumnQuery(connection,'select typo from typos where typo = "' + term + '"')
    itypo_actual = readSingleColumnQuery(connection,'select itypo from itypos where itypo = "' + term + '"')
    typo_id = readSingleColumnQuery(connection,'select typo from typos where typo_id = "' + term + '"')
    itypo_id = readSingleColumnQuery(connection,'select itypo from itypos where itypo_id = "' + term + '"')
    csep_id = readSingleColumnQuery(connection,'select csep from cseps where csep_id = "' + term + '"')

    if(len(Jap) > 0 and force_return_value == None or force_return_value == "JAP"):

        print("------------------------------------------------\njValue\n------------------------------------------------")

        wordid_j = readSingleColumnQuery(connection,'select word_id from words where jValue = "' + term + '"')

        if(len(Jap) > 1):

            print(Jap,end="\n")
            print(wordid_j)
            index = input("\nPlease input the index of the jValue you are looking for")
            term = Jap[index]
            word_id = wordid_j[index]

        else:

            term = Jap[0]
            word_id = wordid_j[0]
            
        jr_j = readSingleColumnQuery(connection,'select jrValue from words where word_id = ' + word_id)
        Eng_j = readSingleColumnQuery(connection,'select eValue from words where word_id = ' + word_id)
        Furi_j = readSingleColumnQuery(connection,'select fValue from words where word_id = ' + word_id)
        corr_j = readSingleColumnQuery(connection,'select cValue from words where word_id = ' + word_id)
        prob_j = readSingleColumnQuery(connection,'select pValue from words where word_id = ' + word_id)
        cSEP_j = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + word_id)

        print("id : " +word_id)
        print("jValue : " + term)
        print("jrValue : " + jr_j[0])
        print("eValue : " + Eng_j[0])
        print("fValue : " + Furi_j[0])
        print("cValue : " + corr_j[0])
        print("pValue : " + prob_j[0] + "\nValid Cseps : ",end = '')
        print(cSEP_j)

        if(force_return_value == "JAP"):
            os.system('pause')
            return

    if(len(Eng) > 0 and force_return_value == None or force_return_value == "ENG"):

        print("------------------------------------------------\neValue\n------------------------------------------------")

        wordid_e = readSingleColumnQuery(connection,'select word_id from words where eValue = "' + term + '"')

        if(len(Eng) > 1):

            print(Eng,end="\n")
            print(wordid_e)
            index = input("\nPlease input the index of the eValue you are looking for")
            term = Eng[index]
            word_id = wordid_e[index]

        else:
            
            term = Eng[0]
            word_id = wordid_e[0]
            
        jr_e = readSingleColumnQuery(connection,'select jrValue from words where word_id = ' + word_id)
        Jap_e = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + word_id)
        Furi_e = readSingleColumnQuery(connection,'select fValue from words where word_id = ' + word_id)
        corr_e = readSingleColumnQuery(connection,'select cValue from words where word_id = ' + word_id)
        prob_e = readSingleColumnQuery(connection,'select pValue from words where word_id = ' + word_id)
        cSEP_e = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + word_id)

        print("id : " + word_id)
        print("jValue : " + Jap_e[0])
        print("jrValue : " + jr_e[0])
        print("eValue : " + term)
        print("fValue : " + Furi_e[0])
        print("cValue : " + corr_e[0])
        print("pValue : " + prob_e[0] + "\nValid Cseps : ",end = '')
        print(cSEP_e)

        if(force_return_value == "ENG" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="ENG"):
            return
        else:
            pass

    if(len(Jap_roma) > 0 and force_return_value == None or force_return_value == "JAP_ROMA"):

        print("------------------------------------------------\njrValue\n------------------------------------------------")

        wordid_jr = readSingleColumnQuery(connection,'select word_id from words where jrValue = "' + term + '"')

        if(len(Jap_roma) > 1):

            print(Jap_roma,end="\n")
            print(wordid_jr)
            index = input("\nPlease input the index of the jrValue you are looking for")
            term = Jap_roma[index]
            word_id = wordid_jr[index]

        else:
            
            term = Jap_roma[0]
            word_id = wordid_jr[0]
            
        Jap_jr = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + word_id)
        Eng_jr = readSingleColumnQuery(connection,'select eValue from words where word_id = ' + word_id)
        Furi_jr = readSingleColumnQuery(connection,'select fValue from words where word_id = ' + word_id)
        corr_jr = readSingleColumnQuery(connection,'select cValue from words where word_id = ' + word_id)
        prob_jr = readSingleColumnQuery(connection,'select pValue from words where word_id = ' + word_id)
        cSEP_jr = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + word_id)

        print("id : " +word_id)
        print("jValue : " + Jap_jr[0])
        print("jrValue : " + term)
        print("eValue : " + Eng_jr[0])
        print("fValue : " + Furi_jr[0])
        print("cValue : " + corr_jr[0])
        print("pValue : " + prob_jr[0] + "\nValid Cseps : ",end = '')
        print(cSEP_jr)

        if(force_return_value == "JAP_ROMA" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="JAP_ROMA"):
            return
        else:
            pass

    if(len(Furi) > 0 and force_return_value == None or force_return_value == "FURI"):

        print("------------------------------------------------\nfValue\n------------------------------------------------")

        wordid_f = readSingleColumnQuery(connection,'select word_id from words where fValue != 0 and fValue = "' + term + '"')

        if(len(Furi) > 1):

            print(Furi,end="\n")
            print(wordid_f)
            index = input("\nPlease input the index of the fValue you are looking for")
            term = Furi[index]
            word_id = wordid_f[index]

        else:
            
            term = Furi[0]
            word_id = wordid_f[0]
            
        Jap_f = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + word_id)
        Eng_f = readSingleColumnQuery(connection,'select eValue from words where word_id = ' + word_id)
        Jap_roma_f = readSingleColumnQuery(connection,'select jrValue from words where word_id = ' + word_id)
        corr_f = readSingleColumnQuery(connection,'select cValue from words where word_id = ' + word_id)
        prob_f = readSingleColumnQuery(connection,'select pValue from words where word_id = ' + word_id)
        cSEP_f = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + word_id)

        print("id : " + word_id)
        print("jValue : " + Jap_f[0])
        print("jrValue : " + Jap_roma_f[0])
        print("eValue : " + Eng_f[0])
        print("fValue : " + term)
        print("cValue : " + corr_f[0])
        print("pValue : " + prob_f[0] + "\nValid Cseps : ",end = '')
        print(cSEP_f)

        if(force_return_value == "FURI" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="FURI"):
            return
        else:
            pass

    if(len(prob) > 0 and force_return_value == None or force_return_value == "PROB"):

        print("------------------------------------------------\npValue\n------------------------------------------------")

        wordid_p = readSingleColumnQuery(connection,'select word_id from words where pValue = "' + term + '"')

        print("Number of words with a pValue of " + term + " : " + str(len(prob)),end="\n")
        print("Word_ids with a pValue of : " + term)
        print(wordid_p)

        if(force_return_value == "PROB" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="PROB"):
            return
        else:
            pass

    if(len(corr) > 0 and force_return_value == None or force_return_value == "CORR"):

        print("------------------------------------------------\ncValue\n------------------------------------------------")

        wordid_c = readSingleColumnQuery(connection,'select word_id from words where cValue = "' + term + '"')

        print("Number of words with a cValue of " + term + " : " + str(len(corr)),end="\n")
        print("Word_ids with a cValue of : " + term)
        print(wordid_c)

        if(force_return_value == "CORR" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="CORR"):
            return
        else:
            pass

    if(len(word_id) > 0 and term.isnumeric() == True and force_return_value == None or force_return_value == "WORD_ID"):

        print("------------------------------------------------\nWORD_ID\n------------------------------------------------")
            
        Jap_i = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + term)
        jr_i = readSingleColumnQuery(connection,'select jrValue from words where word_id = ' + term)
        Eng_i = readSingleColumnQuery(connection,'select eValue from words where word_id = ' + term)
        Furi_i = readSingleColumnQuery(connection,'select fValue from words where word_id = ' + term)
        corr_i = readSingleColumnQuery(connection,'select cValue from words where word_id = ' + term)
        prob_i = readSingleColumnQuery(connection,'select pValue from words where word_id = ' + term)
        cSEP_i = readSingleColumnQuery(connection,'select csep from cseps where word_id = ' + term)

        print("word_id : " + term)
        print("jValue : " + Jap_i[0])
        print("jrValue : " + jr_i[0])
        print("eValue : " + Eng_i[0])
        print("fValue : " + Furi_i[0])
        print("cValue : " + corr_i[0])
        print("pValue : " + prob_i[0] + "\nValid Cseps : ",end = '')
        print(cSEP_i)

        if(force_return_value == "WORD_ID" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="WORD_ID"):
            return
        else:
            pass

    if(len(csep_id) > 0 and force_return_value == None or force_return_value == "CSEP_ID"):

        print("------------------------------------------------\nCSEP_ID\n------------------------------------------------")

        wordid_csep = readSingleColumnQuery(connection,'select word_id from cseps where csep_id = "' + term + '"')
            
        jap_csep = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + wordid_csep[0])
        jr_csep = readSingleColumnQuery(connection,'select jrValue from words where word_id = ' + wordid_csep[0])
        Eng_csep = readSingleColumnQuery(connection,'select eValue from words where word_id = ' + wordid_csep[0])
        cSEP_csep = readSingleColumnQuery(connection,'select csep from cseps where csep_id = ' + term)

        print("csep_id : " + term)
        print("word id : " + wordid_csep[0])
        print("jValue : " + jap_csep[0])
        print("jrValue : " + jr_csep[0])
        print("eValue : " + Eng_csep[0])
        print("CSEP : " + cSEP_csep[0])

        if(force_return_value == "CSEP_ID" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="CSEP_ID"):
            return
        else:
            pass

    if(len(csep_line) > 0 and force_return_value == None or force_return_value == "CSEP_LINE"):

        print("------------------------------------------------\nCSEP_LINE\n------------------------------------------------")

        print("CSEP Line for word_id : " + term)

        csep_csep_line = readSingleColumnQuery(connection,'select csep from cseps where word_id = "' + term + '"')
        csep_id_line = readSingleColumnQuery(connection,'select csep_id from cseps where word_id = "' + term + '"')
            
        print("\nCSEP Line : ",end="")
        print(csep_csep_line)

        print("\nCSEP ID Line : ",end="")
        print(csep_id_line)

        if(force_return_value == "CSEP_LINE" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="CSEP_LINE"):
            return
        else:
            pass

    if(len(typo_id) > 0 and force_return_value == None or force_return_value == "TYPO_ID"):

        print("------------------------------------------------\nTYPO_ID\n------------------------------------------------")
            
        typo_t = readSingleColumnQuery(connection,'select typo from typos where typo_id = ' + term)
        word_id_t = readSingleColumnQuery(connection,'select word_id from typos where typo_id = ' + term)

        print("typo id : " + term)
        print("word_id : " + word_id_t[0])
        print("typo : " + typo_t[0])

        if(force_return_value == "TYPO_ID" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="TYPO_ID"):
            return
        else:
            pass

    if(len(itypo_id) > 0 and force_return_value == None or force_return_value == "ITYPO_ID"):

        print("------------------------------------------------\nITYPO_ID\n------------------------------------------------")
            
        itypo_it = readSingleColumnQuery(connection,'select itypo from itypos where itypo_id = ' + term)
        word_id_it = readSingleColumnQuery(connection,'select word_id from itypos where itypo_id = ' + term)

        print("itypo id : " + term)
        print("word_id : " + word_id_it[0])
        print("itypo : " + itypo_it[0])

        if(force_return_value == "ITYPO_ID" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="ITYPO_ID"):
            return
        else:
            pass

    if(len(typo_actual) > 0 and force_return_value == None or force_return_value == "TYPO_ACTUAL"):

        i = 0

        print("------------------------------------------------\nTYPO_ACTUAL\n------------------------------------------------")

        word_id_typo = readSingleColumnQuery(connection,'select word_id from typos where typo = "' + term + '"')
        typo_id_typo = readSingleColumnQuery(connection,'select typo_id from typos where typo = "' + term + '"')
        jap_typo = []

        while(i < len(word_id_typo)):
            temp = readSingleColumnQuery(connection,'select jValue from words where word_id = "' + word_id_typo[i] + '"')
            jap_typo += temp
            i+=1

        if(len(typo_actual) > 1):

            print(typo_actual)
            print(word_id_typo)
            print(jap_typo)

            index = input("\nPlease input the index of the typo you are looking for")
            term = typo_actual[index]
            word_id = word_id_typo[index]
            typo_id = typo_id_typo[index]

        else:
            
            term = typo_actual[0]
            word_id = word_id_typo[0]
            typo_id = typo_id_typo[0]

        print("word id : " + word_id)
        print("typo id : " + typo_id)
        print("typo : " + term)

        if(force_return_value == "TYPO_ACUTAL" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="TYPO_ACTUAL"):
            return
        else:
            pass

    if(len(itypo_actual) > 0 and force_return_value == None or force_return_value == "ITYPO_ACTUAL"):

        i = 0

        print("------------------------------------------------\nITYPO_ACTUAL\n------------------------------------------------")

        word_id_itypo = readSingleColumnQuery(connection,'select word_id from itypos where itypo = "' + term + '"')
        itypo_id_itypo = readSingleColumnQuery(connection,'select itypo_id from itypos where itypo = "' + term + '"')
        jap_itypo = []

        while(i < len(word_id_itypo)):
            temp = readSingleColumnQuery(connection,'select jValue from words where word_id = "' + word_id_itypo[i] + '"')
            jap_itypo += temp
            i+=1

        if(len(itypo_actual) > 1):

            print(itypo_actual)
            print(word_id_itypo)
            print(jap_itypo)

            index = input("\nPlease input the index of the typo you are looking for")
            term = itypo_actual[index]
            word_id = word_id_itypo[index]
            itypo_id = itypo_id_itypo[index]

        else:
            
            term = itypo_actual[0]
            word_id = word_id_itypo[0]
            itypo_id = itypo_id_itypo[0]

        print("word id : " + word_id)
        print("itypo id : " + itypo_id)
        print("itypo : " + term)


        if(force_return_value == "ITYPO_ACUTAL" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="ITYPO_ACTUAL"):
            return
        else:
            pass

    if(len(csep_actual) > 0 and force_return_value == None or force_return_value == "CSEP_ACTUAL"):

        i = 0

        print("------------------------------------------------\nCSEP_ACTUAL\n------------------------------------------------")

        word_id_csep_actual = readSingleColumnQuery(connection,'select word_id from cseps where csep = "' + term + '"')
        csep_id_csep_actual = readSingleColumnQuery(connection,'select csep_id from cseps where csep = "' + term + '"')
        jap_csep_actual = []

        while(i < len(word_id_csep_actual)):
            temp = readSingleColumnQuery(connection,'select jValue from words where word_id = "' + word_id_csep_actual[i] + '"')
            jap_csep_actual += temp
            i+=1

        if(len(itypo_actual) > 1):

            print(csep_actual)
            print(word_id_csep_actual)
            print(jap_csep_actual)

            index = input("\nPlease input the index of the typo you are looking for")
            term = csep_actual[index]
            word_id = word_id_csep_actual[index]
            csep_id = csep_id_csep_actual[index]

        else:
            
            term = csep_actual[0]
            word_id = word_id_csep_actual[0]
            csep_id = csep_id_csep_actual[0]

        Jap = readSingleColumnQuery(connection,'select jValue from words where word_id = ' + word_id) 

        print("word id : " + word_id)
        print("csep id : " + csep_id)
        print("jValue : " + Jap[0])
        print("csep : " + term)


        if(force_return_value == "CSEP_ACTUAL" and pause_value == 1):
            os.system('pause')
            return
        elif(force_return_value =="CSEP_ACTUAL"):
            return
        else:
            pass

    print("\n")
    os.system('pause')

#-------------------Start-of-ecset()---------------------------------------------------------

def ecset(targetLine, columnNum, uInput, filePath):
    with open(filePath, "r+", encoding="utf8") as f:
        lines = f.readlines()

    line = lines[targetLine]

    items = line.split(",")
    items[columnNum - 1] = repr(uInput)

    new_line = ",".join(items)

    lines[targetLine] = new_line

    with open(filePath, "w", encoding="utf8") as f:
        f.writelines(lines)

#-------------------Start-of-clearStream()-------------------------------------------------

def clearStream():
    
    while msvcrt.kbhit():
        msvcrt.getch()
        
    sleep(0.07) 

#-------------------Start-of-userConfirm()-------------------------------------------------

def userConfirm(ucPrompt,ucConfirm1,ucConfirm2):

    entryConfirmed = False
    ucConfirm3 = ""
    
    while(entryConfirmed == False):

        os.system('cls')
        
        clearStream()
        
        userInput = input(ucPrompt)
        
        if(userInput == "q"):
            exit()

        assert userInput != "z"

        ucConfirm3 = ucConfirm1 + userInput + ucConfirm2
        os.system('cls')
        
        print(ucConfirm3)
        clearStream()
        
        if(int(inputCheck(4,key.read_key(),2,ucConfirm3)) == 1):
                entryConfirmed = True
        else:
            os.system('cls')
            
            print(ucPrompt)
            
            ucConfirm3 = ""

    os.system('cls')

    return userInput
       
#--------------------start of inputCheck()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def inputCheck(iType, userInput, numChoices, inputPromptMsg):

    userInput = str(userInput)
    newUserI = str(userInput)
    inputIssueMsg = ""

    os.system('cls')

    while True:
        if userInput == 'q':
            exit()
        elif userInput == 'v' and iType != 1:
            return newUserI
        elif iType == 1 and (userInput.isdigit() == False or userInput == "0"):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q'\n"
        elif iType == 4 and (userInput.isdigit() == False or int(userInput) > numChoices):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"
        elif iType == 5 and (userInput.isdigit() == False or int(userInput) > numChoices):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"
        else:
            return newUserI

        if iType == 5:
            print(inputIssueMsg + "\n")
            userInput = input(inputPromptMsg)
        else:
            print(inputIssueMsg + "\n" + inputPromptMsg)
            userInput = key.read_key()

        os.system('cls')
        clearStream()
        newUserI = str(userInput)

    return str(newUserI)

#-------------------start of readLoopData()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def readLoopData(column):
    file1 = open(r"C:\ProgramData\SJLT\loopData.txt", "r",encoding="utf8")
    raw_s= file1.read()
    file1.close()

    count = raw_s.count(',')
    i,ii = 0,0
    buildStr = ""
    stats = []

    while(i < count):
        if(raw_s[ii] != ","):
            buildStr += raw_s[ii]
        else:
            stats.append(buildStr)
            buildStr = ""
            i+=1
        ii+=1
        
    return int(stats[column-1])

#--------------------Start-of-addToItypos()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addToItypos(itypo, word_id, itypo_id, connection):
    cursor = connection.cursor()

    query ="""
    INSERT INTO itypos (itypo_id, word_id, itypo)
    VALUES (%s, %s, %s)
    """
    values = (itypo_id,word_id,itypo.lower())
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    
#--------------------Start-of-addToTypos()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addToTypos(typo, word_id, typo_id, connection):
    cursor = connection.cursor()

    query ="""
    INSERT INTO typos (typo_id, word_id, typo)
    VALUES (%s, %s, %s)
    """
    values = (typo_id,word_id,typo.lower())    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()


#--------------------Start-of-deleteValue()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def deleteValue(connection,target_id):

        word = readSingleColumnQuery(connection,'select word_id from words where word_id = "' + target_id + '"')
        csep = readSingleColumnQuery(connection,'select csep_id from cseps where csep_id = "' + target_id + '"')
        typo = readSingleColumnQuery(connection,'select typo_id from typos where typo_id = "' + target_id + '"')
        itypo = readSingleColumnQuery(connection,'select itypo_id from itypos where itypo_id = "' + target_id + '"')

        w_length = len(word)
        c_length = len(csep)
        i_length = len(typo)
        it_length = len(itypo)

        if(w_length == 1):
            print("Nusevei has confirmed the existence of a word with an id of " + target_id)
            search(target_id,connection,"WORD_ID",None)
        if(c_length == 1):
            print("Nusevei has confirmed the existence of a csep with an id of " + target_id)
            search(target_id,connection,"CSEP_ID",None)
        if(i_length == 1):
            print("Nusevei has confirmed the existence of a typo with an id of " + target_id)
            search(target_id,connection,"TYPO_ID",None)
        if(it_length == 1):
            print("Nusevei has confirmed the existence of a itypo with an id of " + target_id,)
            search(target_id,connection,"ITYPO_ID",None)

        print("\n")

        if(w_length == 1):
            print("Nusevei has confirmed the existence of a word with an id of " + target_id + ", Press 1 to select this.\n")
        if(c_length == 1):
            print("Nusevei has confirmed the existence of a csep with an id of " + target_id + ", Press 2 to select this.\n")
        if(i_length == 1):
            print("Nusevei has confirmed the existence of a typo with an id of " + target_id + ", Press 3 to select this.\n")
        if(it_length == 1):
            print("Nusevei has confirmed the existence of a itypo with an id of " + target_id + ", Press 4 to select this.\n")

        sleep(.7)

        path = key.read_key()

        if(path == "1"):
            delete(connection,'words','word_id',str(target_id))
            delete(connection,'cseps','word_id',str(target_id))
        elif(path == "2"):
            delete(connection,'cseps','csep_id',str(target_id))
        elif(path == "3"):
            delete(connection,'typos','typo_id',str(target_id))
        elif(path == "4"):
            delete(connection,'itypos','itypo_id',str(target_id))
        else:
            pass

#--------------------Start-of-replaceValue()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def replaceValue(typeReplacement,connection,target_id):

        if(typeReplacement == "1"):
            print("Please select which value you would like to replace")
            print("\n1. jValue = ",end="") 
            print(readSingleColumnQuery(connection,'select jValue from words where word_id = "' + target_id + '"'))
            print("\n2. jrValue = ",end="") 
            print(readSingleColumnQuery(connection,'select jrValue from words where word_id = "' + target_id + '"'))
            print("\n3. eValue = ",end="") 
            print(readSingleColumnQuery(connection,'select eValue from words where word_id = "' + target_id + '"'))
            print("\n4. fValue",end="") 
            print(readSingleColumnQuery(connection,'select fValue from words where word_id = "' + target_id + '"'))
            print("\n5. pValue",end="") 
            print(readSingleColumnQuery(connection,'select pValue from words where word_id = "' + target_id + '"'))
            print("\n6. cValue",end="") 
            print(readSingleColumnQuery(connection,'select cValue from words where word_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()
            
            clearStream()
            os.system('cls')

            value = userConfirm("What would you like to replace it with?\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")


            if(path == "1"):
                target = "jValue"
            elif(path == "2"):
                target = "jrValue"
            elif(path == "3"):
                target = "eValue"
            elif(path == "4"):
                target = "fValue"
            elif(path == "5"):
                target = "pValue"
            elif(path == "6"):
                target = "cValue"
            else:
                exit()
            
            executeQuery(connection,'update words set ' + target + ' = "' + value + '" where word_id = ' + target_id)

        elif(typeReplacement == "2"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(readSingleColumnQuery(connection,'select word_id from cseps where csep_id = "' + target_id + '"'))
            print("\n2. csep = ",end="") 
            print(readSingleColumnQuery(connection,'select csep from cseps where csep_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clearStream()
            os.system('cls')
            
            value = userConfirm("What would you like to replace it with?\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "csep"
            else:
                exit()
            
            executeQuery(connection,'update cseps set ' + target + ' = "' + value + '" where csep_id = ' + target_id)

        elif(typeReplacement == "3"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(readSingleColumnQuery(connection,'select word_id from typos where typo_id = "' + target_id + '"'))
            print("\n2. typo = ",end="") 
            print(readSingleColumnQuery(connection,'select typo from typos where typo_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clearStream()
            os.system('cls')
            
            value = userConfirm("What would you like to replace it with?\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "typo"
            else:
                exit()
            
            executeQuery(connection,'update typos set ' + target + ' = "' + value + '" where typo_id = ' + target_id)

        elif(typeReplacement == "4"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(readSingleColumnQuery(connection,'select word_id from itypos where itypo_id = "' + target_id + '"'))
            print("\n2. itypo = ",end="") 
            print(readSingleColumnQuery(connection,'select itypo from itypos where itypo_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clearStream()
            os.system('cls')
            
            value = userConfirm("What would you like to replace it with?\n","Just To Confirm You Selected "," Press 1 To Confirm or 2 To Retry")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "itypo"
            else:
                exit()
            
            executeQuery(connection,'update itypos set ' + target + ' = "' + value + '" where itypo_id = ' + target_id)

#--------------------Start-of-createConnection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def createConnection(host_name, user_name, user_password,db_name):

    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database= db_name)

    return connection

#--------------------Start-of-executeQuery()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def executeQuery(connection, query):
    
    cursor = connection.cursor()
    cursor.execute(query)
    
    connection.commit()

#--------------------Start-of-readSingleColumnQuery()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def readSingleColumnQuery(connection, query):
    
    cursor = connection.cursor()
    resultsActual = []
    i = 0

    cursor.execute(query)
    results = cursor.fetchall()

    resultsActual = [str(i[0]) for i in results]

    return resultsActual

#--------------------Start-of-readMultiColumnQuery()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def readMultiColumnQuery(connection, query):

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    if(len(results) == 0):
        return [[]] * cursor.description.__len__()

    resultsByColumn = [[] for i in range(len(results[0]))]
    
    for row in results:
        for i, value in enumerate(row):
            resultsByColumn[i].append(str(value))

    return resultsByColumn


#--------------------Start-of-readQueryRaw()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def readQueryRaw(connection, query):
    
    cursor = connection.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    return results

#--------------------Start-of-addToJSET()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addToJSET(jValue, jrValue, eValue, fValue, pValue, cValue, word_id, word_type, connection):
    
    cursor = connection.cursor()

    query ="""
    INSERT INTO words (word_id, jValue, jrValue, eValue, fValue, pValue, cValue, word_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (word_id, jValue.lower(), jrValue.lower(), eValue.lower(), fValue, pValue, cValue, word_type)
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()

#--------------------Start-of-addToCSEP()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addToCSEP(csep, word_id, csep_id, connection):
    cursor = connection.cursor()

    query ="""
    INSERT INTO cseps (csep_id, word_id, csep)
    VALUES (%s, %s, %s)
    """
    values = (csep_id, word_id, csep.lower())
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()

#--------------------Start-of-delete()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def delete(connection,table,row,Id):
    cursor = connection.cursor()

    query = 'delete from ' + table + ' where ' + row + ' = ' + Id

    cursor.execute(query)

    connection.commit()

    cursor.close()
