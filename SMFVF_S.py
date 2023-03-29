import os  
import keyboard as key
import msvcrt
import mysql.connector

from time import sleep

#-------------------Start-of-search()---------------------------------------------------------

def search(term,connection,forceReturnValue,pauseValue):

    jap = read_single_column_query(connection,'select jValue from words where jValue = "' + term + '"')
    japRoma = read_single_column_query(connection,'select jrValue from words where jrValue = "' + term + '"')
    eng = read_single_column_query(connection,'select eValue from words where eValue = "' + term + '"')
    furi = read_single_column_query(connection,'select fValue from words where fValue != 0 and fValue = "' + term + '"')
    corr = read_single_column_query(connection,'select cValue from words where cValue = "' + term + '"')
    prob = read_single_column_query(connection,'select pValue from words where pValue = "' + term + '"')
    csepLine = read_single_column_query(connection,'select csep from cseps where csep_id = "' + term + '"')
    csepActual = read_single_column_query(connection,'select csep from cseps where csep = "' + term + '"')
    word_id = read_single_column_query(connection,'select jValue from words where word_id = "' + term + '"')
    typoActual = read_single_column_query(connection,'select typo from typos where typo = "' + term + '"')
    itypoActual = read_single_column_query(connection,'select itypo from itypos where itypo = "' + term + '"')
    typo_id = read_single_column_query(connection,'select typo from typos where typo_id = "' + term + '"')
    itypo_id = read_single_column_query(connection,'select itypo from itypos where itypo_id = "' + term + '"')
    csep_id = read_single_column_query(connection,'select csep from cseps where csep_id = "' + term + '"')

    if(len(jap) > 0 and forceReturnValue == None or forceReturnValue == "JAP"):

        print("------------------------------------------------\njValue\n------------------------------------------------")

        word_id_j = read_single_column_query(connection,'select word_id from words where jValue = "' + term + '"')

        if(len(jap) > 1):

            print(jap,end="\n")
            print(word_id_j)
            index = int(input("\nPlease input the index of the jValue you are looking for "))
            term = jap[index]
            word_id = word_id_j[index]

        else:

            term = jap[0]
            word_id = word_id_j[0]
            
        jr_j,eng_j,furi_j,corr_j,prob_j = read_multi_column_query(connection,'select jrValue,eValue,fValue,cValue,pValue from words where word_id = ' + word_id)
        csep_j = read_single_column_query(connection,'select csep from cseps where word_id = ' + word_id)
        csep_line_j = read_single_column_query(connection,'select csep_id from cseps where word_id = ' + word_id)

        print("word_id : " + word_id)
        print("jValue : " + term)
        print("jrValue : " + jr_j[0])
        print("eValue : " + eng_j[0])
        print("fValue : " + furi_j[0])
        print("cValue : " + corr_j[0])
        print("pValue : " + prob_j[0] + "\nValid Cseps : ",end = '')
        print(csep_j)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_j)

        if(forceReturnValue == "JAP" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="JAP"):
            return
        else:
            pass

    if(len(eng) > 0 and forceReturnValue == None or forceReturnValue == "ENG"):

        print("------------------------------------------------\neValue\n------------------------------------------------")

        word_id_e,jap_e = read_multi_column_query(connection,'select word_id,jValue from words where eValue = "' + term + '"')

        if(len(eng) > 1):

            print(eng,end="\n")
            print(jap_e)
            print(word_id_e)
            index = int(input("\nPlease input the index of the eValue you are looking for "))
            term = eng[index]
            word_id = word_id_e[index]

        else:
            
            term = eng[0]
            word_id = word_id_e[0]
            
        jr_e,jap_e,furi_e,corr_e,prob_e = read_multi_column_query(connection,'select jrValue,jValue,fValue,cValue,pValue from words where word_id = ' + word_id)
        csep_e = read_single_column_query(connection,'select csep from cseps where word_id = ' + word_id)
        csep_line_e = read_single_column_query(connection,'select csep_id from cseps where word_id = ' + word_id)

        print("word_id : " + word_id)
        print("jValue : " + jap_e[0])
        print("jrValue : " + jr_e[0])
        print("eValue : " + term)
        print("fValue : " + furi_e[0])
        print("cValue : " + corr_e[0])
        print("pValue : " + prob_e[0] + "\nValid Cseps : ",end = '')
        print(csep_e)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_e)

        if(forceReturnValue == "ENG" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="ENG"):
            return
        else:
            pass

    if(len(japRoma) > 0 and forceReturnValue == None or forceReturnValue == "JAP_ROMA"):

        print("------------------------------------------------\njrValue\n------------------------------------------------")

        word_id_jr = read_single_column_query(connection,'select word_id from words where jrValue = "' + term + '"')

        if(len(japRoma) > 1):

            print(japRoma,end="\n")
            print(word_id_jr)
            index = int(input("\nPlease input the index of the jrValue you are looking for "))
            term = japRoma[index]
            word_id = word_id_jr[index]

        else:
            
            term = japRoma[0]
            word_id = word_id_jr[0]
            
        eng_jr,jap_jr,furi_jr,corr_jr,prob_jr = read_multi_column_query(connection,'select eValue,jValue,fValue,cValue,pValue from words where word_id = ' + word_id)
        csep_jr = read_single_column_query(connection,'select csep from cseps where word_id = ' + word_id)
        csep_line_jr = read_single_column_query(connection,'select csep_id from cseps where word_id = ' + word_id)

        print("word_id : " + word_id)
        print("jValue : " + jap_jr[0])
        print("jrValue : " + term)
        print("eValue : " + eng_jr[0])
        print("fValue : " + furi_jr[0])
        print("cValue : " + corr_jr[0])
        print("pValue : " + prob_jr[0] + "\nValid Cseps : ",end = '')
        print(csep_jr)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_jr)

        if(forceReturnValue == "JAP_ROMA" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="JAP_ROMA"):
            return
        else:
            pass

    if(len(furi) > 0 and forceReturnValue == None or forceReturnValue == "FURI"):

        print("------------------------------------------------\nfValue\n------------------------------------------------")

        word_id_f = read_single_column_query(connection,'select word_id from words where fValue != 0 and fValue = "' + term + '"')

        if(len(furi) > 1):

            print(furi,end="\n")
            print(word_id_f)
            index = int(input("\nPlease input the index of the fValue you are looking for "))
            term = furi[index]
            word_id = word_id_f[index]

        else:
            
            term = furi[0]
            word_id = word_id_f[0]
            
        eng_f,jap_f,japRoma_f,corr_f,prob_f = read_multi_column_query(connection,'select eValue,jValue,jrValue,cValue,pValue from words where word_id = ' + word_id)
        csep_f = read_single_column_query(connection,'select csep from cseps where word_id = ' + word_id)
        csep_line_f = read_single_column_query(connection,'select csep_id from cseps where word_id = ' + word_id)

        print("word_id : " + word_id)
        print("jValue : " + jap_f[0])
        print("jrValue : " + japRoma_f[0])
        print("eValue : " + eng_f[0])
        print("fValue : " + term)
        print("cValue : " + corr_f[0])
        print("pValue : " + prob_f[0] + "\nValid Cseps : ",end = '')
        print(csep_f)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_f)

        if(forceReturnValue == "FURI" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="FURI"):
            return
        else:
            pass

    if(len(prob) > 0 and forceReturnValue == None or forceReturnValue == "PROB"):

        print("------------------------------------------------\npValue\n------------------------------------------------")

        word_id_p = read_single_column_query(connection,'select word_id from words where pValue = "' + term + '"')

        print("Number of words with a pValue of " + term + " : " + str(len(prob)),end="\n")
        print("word_ids with a pValue of : " + term)
        print(word_id_p)

        if(forceReturnValue == "PROB" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="PROB"):
            return
        else:
            pass

    if(len(corr) > 0 and forceReturnValue == None or forceReturnValue == "CORR"):

        print("------------------------------------------------\ncValue\n------------------------------------------------")

        word_id_c = read_single_column_query(connection,'select word_id from words where cValue = "' + term + '"')

        print("Number of words with a cValue of " + term + " : " + str(len(corr)),end="\n")
        print("word_ids with a cValue of : " + term)
        print(word_id_c)

        if(forceReturnValue == "CORR" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="CORR"):
            return
        else:
            pass

    if(len(word_id) > 0 and term.isnumeric() == True and forceReturnValue == None or forceReturnValue == "WORD_ID"):

        print("------------------------------------------------\nWORD_ID\n------------------------------------------------")
            
        jap_i,jr_i,eng_i,furi_i,corr_i,prob_i = read_multi_column_query(connection,'select jValue,jrValue,eValue,fValue,cValue,pValue from words where word_id = ' + term)
        csep_i,csep_line_i = read_multi_column_query(connection,'select csep,csep_id from cseps where word_id = ' + term)

        print("word_id : " + term)
        print("jValue : " + jap_i[0])
        print("jrValue : " + jr_i[0])
        print("eValue : " + eng_i[0])
        print("fValue : " + furi_i[0])
        print("cValue : " + corr_i[0])
        print("pValue : " + prob_i[0] + "\nValid Cseps : ",end = '')
        print(csep_i)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_i)

        if(forceReturnValue == "WORD_ID" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="WORD_ID"):
            return
        else:
            pass

    if(len(csep_id) > 0 and forceReturnValue == None or forceReturnValue == "CSEP_ID"):

        print("------------------------------------------------\nCSEP_ID\n------------------------------------------------")

        word_id_csep,csep_csep = read_multi_column_query(connection,'select word_id,csep from cseps where csep_id = "' + term + '"')

        jap_csep,jr_csep,eng_csep,furi_csep,corr_csep,prob_csep = read_multi_column_query(connection,'select jValue,jrValue,eValue,fValue,cValue,pValue from words where word_id = ' + word_id_csep[0])
        csep_all_csep,csep_line_csep = read_multi_column_query(connection,'select csep,csep_id from cseps where word_id = ' + term)

        print("word_id : " + word_id_csep[0])
        print("jValue : " + jap_csep[0])
        print("jrValue : " + jr_csep[0])
        print("eValue : " + eng_csep[0])
        print("fValue : " + furi_csep[0])
        print("cValue : " + corr_csep[0])
        print("pValue : " + prob_csep[0])
        print("CSEP : " + csep_csep[0])
        print("CSEP ID : " + term + "\nValid Cseps : ",end = '')
        print(csep_all_csep)
        print("\nValid Csep Ids : ",end = '')
        print(csep_line_csep)

        if(forceReturnValue == "CSEP_ID" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="CSEP_ID"):
            return
        else:
            pass

    if(len(csepLine) > 0 and forceReturnValue == None or forceReturnValue == "CSEP_LINE"):

        print("------------------------------------------------\nCSEP_LINE\n------------------------------------------------")

        print("CSEP Line for word_id : " + term)

        csep_line_csep,csep_id_line = read_multi_column_query(connection,'select csep,csep_id from cseps where word_id = "' + term + '"')

        print("\nCSEP Line : ",end="")
        print(csep_line_csep)

        print("\nCSEP ID Line : ",end="")
        print(csep_id_line)

        if(forceReturnValue == "CSEP_LINE" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="CSEP_LINE"):
            return
        else:
            pass

    if(len(typo_id) > 0 and term.isnumeric() == True and forceReturnValue == None or forceReturnValue == "TYPO_ID"):

        print("------------------------------------------------\nTYPO_ID\n------------------------------------------------")
            
        typo_t,word_id_t = read_multi_column_query(connection,'select typo,word_id from typos where typo_id = ' + term)

        print("typo id : " + term)
        print("word_id : " + word_id_t[0])
        print("typo : " + typo_t[0])

        if(forceReturnValue == "TYPO_ID" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="TYPO_ID"):
            return
        else:
            pass

    if(len(itypo_id) > 0 and term.isnumeric() == True and forceReturnValue == None or forceReturnValue == "ITYPO_ID"):

        print("------------------------------------------------\nITYPO_ID\n------------------------------------------------")
            
        itypo_it,word_id_it = read_multi_column_query(connection,'select itypo,word_id from itypos where itypo_id = ' + term)

        print("itypo id : " + term)
        print("word_id : " + word_id_it[0])
        print("itypo : " + itypo_it[0])

        if(forceReturnValue == "ITYPO_ID" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="ITYPO_ID"):
            return
        else:
            pass

    if(len(typoActual) > 0 and forceReturnValue == None or forceReturnValue == "TYPO_ACTUAL"):

        i = 0

        print("------------------------------------------------\nTYPO_ACTUAL\n------------------------------------------------")

        word_id_typo,typo_id_typo = read_multi_column_query(connection,'select word_id,typo_id from typos where typo = "' + term + '"')
        jap_typo = []

        while(i < len(word_id_typo)):
            temp = read_single_column_query(connection,'select jValue from words where word_id = "' + word_id_typo[i] + '"')
            jap_typo += temp
            i+=1

        if(len(typoActual) > 1):

            print(typoActual)
            print(word_id_typo)
            print(jap_typo)

            index = int(input("\nPlease input the index of the typo you are looking for "))
            term = typoActual[index]
            word_id = word_id_typo[index]
            typo_id = typo_id_typo[index]

        else:
            
            term = typoActual[0]
            word_id = word_id_typo[0]
            typo_id = typo_id_typo[0]

        print("word id : " + word_id)
        print("typo id : " + typo_id)
        print("typo : " + term)

        if(forceReturnValue == "TYPO_ACUTAL" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="TYPO_ACTUAL"):
            return
        else:
            pass

    if(len(itypoActual) > 0 and forceReturnValue == None or forceReturnValue == "ITYPO_ACTUAL"):

        i = 0

        print("------------------------------------------------\nITYPO_ACTUAL\n------------------------------------------------")

        word_id_itypo,itypo_id_itypo = read_multi_column_query(connection,'select word_id,itypo_id from itypos where itypo = "' + term + '"')
        jap_itypo = []

        while(i < len(word_id_itypo)):
            temp = read_single_column_query(connection,'select jValue from words where word_id = "' + word_id_itypo[i] + '"')
            jap_itypo += temp
            i+=1

        if(len(itypoActual) > 1):

            print(itypoActual)
            print(word_id_itypo)
            print(jap_itypo)

            index = int(input("\nPlease input the index of the typo you are looking for "))
            term = itypoActual[index]
            word_id = word_id_itypo[index]
            itypo_id = itypo_id_itypo[index]

        else:
            
            term = itypoActual[0]
            word_id = word_id_itypo[0]
            itypo_id = itypo_id_itypo[0]

        print("word id : " + word_id)
        print("itypo id : " + itypo_id)
        print("itypo : " + term)


        if(forceReturnValue == "ITYPO_ACTUAL" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="ITYPO_ACTUAL"):
            return
        else:
            pass

    if(len(csepActual) > 0 and forceReturnValue == None or forceReturnValue == "CSEP_ACTUAL"):

        i = 0

        print("------------------------------------------------\nCSEP_ACTUAL\n------------------------------------------------")

        word_id_csep_actual,csep_id_csep_actual = read_multi_column_query(connection,'select word_id,csep_id from cseps where csep = "' + term + '"')
        jap_csep_actual = []

        while(i < len(word_id_csep_actual)):
            temp = read_single_column_query(connection,'select jValue from words where word_id = "' + word_id_csep_actual[i] + '"')
            jap_csep_actual += temp
            i+=1

        if(len(itypoActual) > 1):

            print(csepActual)
            print(word_id_csep_actual)
            print(jap_csep_actual)

            index = int(input("\nPlease input the index of the typo you are looking for "))
            term = csepActual[index]
            word_id = word_id_csep_actual[index]
            csep_id = csep_id_csep_actual[index]

        else:
            
            term = csepActual[0]
            word_id = word_id_csep_actual[0]
            csep_id = csep_id_csep_actual[0]

        jap = read_single_column_query(connection,'select jValue from words where word_id = ' + word_id) 

        print("word id : " + word_id)
        print("csep id : " + csep_id)
        print("jValue : " + jap[0])
        print("csep : " + term)


        if(forceReturnValue == "CSEP_ACTUAL" and pauseValue == 1):
            os.system('pause')
            return
        elif(forceReturnValue =="CSEP_ACTUAL"):
            return
        else:
            pass

    print("\n")
    os.system('pause')

#-------------------Start-of-ecset()---------------------------------------------------------

def ecset(targetLine, columnNum, userInput, filePath):

    with open(filePath, "r+", encoding="utf8") as f:
        lines = f.readlines()

    line = lines[targetLine]

    items = line.split(",")
    items[columnNum - 1] = repr(userInput,)

    new_line = ",".join(items)

    lines[targetLine] = new_line

    with open(filePath, "w", encoding="utf8") as f:
        f.writelines(lines)

#-------------------Start-of-clear_stream()-------------------------------------------------

def clear_stream():
    
    while msvcrt.kbhit():
        msvcrt.getch()
        
    sleep(0.1) 

#-------------------Start-of-user_confirm()-------------------------------------------------

def user_confirm(prompt):

    confirmation = "Just To Confirm You Selected "
    options = " Press 1 To Confirm or 2 To Retry"
    output = ""
    
    entryConfirmed = False

    while(entryConfirmed == False):

        os.system('cls')
        
        clear_stream()
        
        userInput = input(prompt)
        
        if(userInput == "q"):
            exit()

        assert userInput != "z"

        os.system('cls')

        output = confirmation + userInput + options
        
        print(output)
        
        clear_stream()
        
        if(int(input_check(4,key.read_key(),2,output)) == 1):
                entryConfirmed = True
        else:

            os.system('cls')
            
            print(prompt)
    
    os.system('cls')

    return userInput
       
#--------------------start of input_check()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def input_check(iType, userInput, numChoices, inputPromptMsg):

    newUserI = str(userInput)
    inputIssueMsg = ""

    os.system('cls')

    while(True):

        if(userInput == 'q'):
            exit()
        elif(userInput == 'v' and iType != 1):
            return newUserI
        elif(iType == 1 and (userInput.isdigit() == False or userInput == "0")):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q'\n"
        elif(iType == 4 and (userInput.isdigit() == False or int(userInput) > numChoices)):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"
        elif(iType == 5 and (userInput.isdigit() == False or int(userInput) > numChoices)):
            inputIssueMsg = "Invalid Input, please enter a valid number choice or 'q' or 'v'\n"
        else:
            return newUserI

        if(iType == 5):
            print(inputIssueMsg + "\n")
            userInput = input(inputPromptMsg)
        else:
            print(inputIssueMsg + "\n" + inputPromptMsg)
            userInput = key.read_key()

        os.system('cls')
        clear_stream()

        newUserI = str(userInput)

#-------------------start of read_loop_data()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_loop_data(column):

    with open(r"C:\ProgramData\SJLT\loopData.txt", "r", encoding="utf-8") as file:
        loopData = file.read()

    count = loopData.count(',')
    i,ii = 0,0
    buildStr = ""
    stats = []

    while(i < count):
        if(loopData[ii] != ","):
            buildStr += loopData[ii]
        else:
            stats.append(buildStr)
            buildStr = ""
            i+=1
        ii+=1
        
    return int(stats[column-1])

#--------------------Start-of-add_to_Itypos()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_to_Itypos(itypo, word_id, itypo_id, connection):
    cursor = connection.cursor()

    query ="""
    insert into itypos (itypo_id, word_id, itypo)
    values (%s, %s, %s)
    """
    values = (itypo_id,word_id,itypo.lower())
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    
#--------------------Start-of-add_to_Typos()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_to_Typos(typo, word_id, typo_id, connection):
    cursor = connection.cursor()

    query ="""
    insert into typos (typo_id, word_id, typo)
    values (%s, %s, %s)
    """
    values = (typo_id,word_id,typo.lower())    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()

#--------------------Start-of-delete_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_value(connection,target_id):

        word = read_single_column_query(connection,'select word_id from words where word_id = "' + target_id + '"')
        csep = read_single_column_query(connection,'select csep_id from cseps where csep_id = "' + target_id + '"')
        typo = read_single_column_query(connection,'select typo_id from typos where typo_id = "' + target_id + '"')
        itypo = read_single_column_query(connection,'select itypo_id from itypos where itypo_id = "' + target_id + '"')

        wLength = len(word)
        cLength = len(csep)
        iLength = len(typo)
        itLength = len(itypo)

        if(wLength == 1):
            print("Nusevei has confirmed the existence of a word with an id of " + target_id)
            search(target_id,connection,"WORD_ID",None)
        if(cLength == 1):
            print("Nusevei has confirmed the existence of a csep with an id of " + target_id)
            search(target_id,connection,"CSEP_ID",None)
        if(iLength == 1):
            print("Nusevei has confirmed the existence of a typo with an id of " + target_id)
            search(target_id,connection,"TYPO_ID",None)
        if(itLength == 1):
            print("Nusevei has confirmed the existence of a itypo with an id of " + target_id,)
            search(target_id,connection,"ITYPO_ID",None)

        print("\n")

        if(wLength == 1):
            print("Nusevei has confirmed the existence of a word with an id of " + target_id + ", Press 1 to select this.\n")
        if(cLength == 1):
            print("Nusevei has confirmed the existence of a csep with an id of " + target_id + ", Press 2 to select this.\n")
        if(iLength == 1):
            print("Nusevei has confirmed the existence of a typo with an id of " + target_id + ", Press 3 to select this.\n")
        if(itLength == 1):
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

#--------------------Start-of-replace_value()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def replace_value(typeReplacement,connection,target_id):
        
        target = None

        if(typeReplacement == "1"):
            print("Please select which value you would like to replace")
            print("\n1. jValue = ",end="") 
            print(read_single_column_query(connection,'select jValue from words where word_id = "' + target_id + '"'))
            print("\n2. jrValue = ",end="") 
            print(read_single_column_query(connection,'select jrValue from words where word_id = "' + target_id + '"'))
            print("\n3. eValue = ",end="") 
            print(read_single_column_query(connection,'select eValue from words where word_id = "' + target_id + '"'))
            print("\n4. fValue",end="") 
            print(read_single_column_query(connection,'select fValue from words where word_id = "' + target_id + '"'))
            print("\n5. pValue",end="") 
            print(read_single_column_query(connection,'select pValue from words where word_id = "' + target_id + '"'))
            print("\n6. cValue",end="") 
            print(read_single_column_query(connection,'select cValue from words where word_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()
            
            clear_stream()
            os.system('cls')

            value = user_confirm("What would you like to replace it with?\n")

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
    
            if(target != None):
                execute_query(connection,'update words set ' + target + ' = "' + value + '" where word_id = ' + target_id)

        elif(typeReplacement == "2"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(read_single_column_query(connection,'select word_id from cseps where csep_id = "' + target_id + '"'))
            print("\n2. csep = ",end="") 
            print(read_single_column_query(connection,'select csep from cseps where csep_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clear_stream()
            os.system('cls')
            
            value = user_confirm("What would you like to replace it with?\n")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "csep"
            
            if(target != None):
                execute_query(connection,'update cseps set ' + target + ' = "' + value + '" where csep_id = ' + target_id)

        elif(typeReplacement == "3"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(read_single_column_query(connection,'select word_id from typos where typo_id = "' + target_id + '"'))
            print("\n2. typo = ",end="") 
            print(read_single_column_query(connection,'select typo from typos where typo_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clear_stream()
            os.system('cls')
            
            value = user_confirm("What would you like to replace it with?\n")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "typo"
            
            if(target != None):
                execute_query(connection,'update typos set ' + target + ' = "' + value + '" where typo_id = ' + target_id)

        elif(typeReplacement == "4"):
            print("Please select which value you would like to replace")
            print("\n1. word_id = ",end="") 
            print(read_single_column_query(connection,'select word_id from itypos where itypo_id = "' + target_id + '"'))
            print("\n2. itypo = ",end="") 
            print(read_single_column_query(connection,'select itypo from itypos where itypo_id = "' + target_id + '"'))

            sleep(.7)

            path = key.read_key()

            clear_stream()
            os.system('cls')
            
            value = user_confirm("What would you like to replace it with?\n")

            if(path == "1"):
                target = "word_id"
            elif(path == "2"):
                target = "itypo"

            if(target != None):
                execute_query(connection,'update itypos set ' + target + ' = "' + value + '" where itypo_id = ' + target_id)

#--------------------Start-of-create_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_connection(host_name, user_name, user_password,db_name):

    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database= db_name)

    return connection

#--------------------Start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def execute_query(connection, query):
    
    cursor = connection.cursor()
    cursor.execute(query)
    
    connection.commit()

#--------------------Start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_single_column_query(connection, query):
    
    cursor = connection.cursor()
    resultsActual = []
    i = 0

    cursor.execute(query)
    results = cursor.fetchall()

    resultsActual = [str(i[0]) for i in results]

    return resultsActual

#--------------------Start-of-read_multi_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_multi_column_query(connection, query):

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


#--------------------Start-of-read_raw_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_raw_query(connection, query):
    
    cursor = connection.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    return results

#--------------------Start-of-add_to_JSET()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_to_JSET(jValue, jrValue, eValue, fValue, pValue, cValue, word_id, word_type, connection):
    
    cursor = connection.cursor()

    query ="""
    insert into words (word_id, jValue, jrValue, eValue, fValue, pValue, cValue, word_type)
    values (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (word_id, jValue.lower(), jrValue.lower(), eValue.lower(), fValue, pValue, cValue, word_type)
    
    cursor.execute(query, values)

    connection.commit()

    cursor.close()

#--------------------Start-of-add_to_CSEP()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_to_CSEP(csep, word_id, csep_id, connection):
    cursor = connection.cursor()

    query ="""
    insert into cseps (csep_id, word_id, csep)
    values (%s, %s, %s)
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
