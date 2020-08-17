#Pygame-Krypto-v3 by Andrew McGilp (c)2020
#
#Turn your Raspberry Pi-3/4 into the ***ENIGMA***
#Note you must use the same pi OS to encode and decode!!

#Important!
#You must create two folders named!!
#  (1) 'Images' then copy River1.png & JedRally.png into it, and
#  (2) 'Settings' then copy Bg1.png image into it

"""
  Notice:

  Please note that this software is used entirely at your own RISK and comes with 
  absolutely no guarantee or warrantee what so ever and by using this software 
  you agree to these terms. It is free to be used by a private individual but not
  free to be used by any (Company, Organisation, Government, etc).
  You may copy and distribute verbatim copies for free but not free for any commercial
  use without permission. changing the code is not allowed without permission.
  
"""

import pygame, time, io, sys, os
import base64, random, copy, glob

from copy import deepcopy
from pygame.locals import *
from io import BytesIO

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 32)
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 32) 

pygame.display.set_caption('Pygame KRYPTO-v4.12')
FPS = pygame.time.Clock()
pygame.mouse.set_visible(True)

#Color    R    G    B   Display font colors
WHITE = (225, 225, 225)#Display color White
RED = (200, 50, 50)#Display color Red
GREEN = (80, 200, 80)#Display color Green
ORANGE = (150, 150, 10)#Display color Orange
BLACK = (10, 10 ,10)
BZLCOL = RED

LEFT = 1
MIDDLE = 2
RIGHT = 3
UP = 4
DOWN = 5

genJunk = True #True to gen dummy chars set (genJunk = False & imgMode = 2) to read user file
capsOn = False
done = False
canI = False
iCan = False
showImg = True
conDel = False
debug = False
imgCount = 0
editMode = 0
indexNo = 0
listNo = 0
useImgName = True

#Default_User_Settings----------0
strKey = '' #Your Public-Key/Public-Name
strPath = 'eDocs/' #Preset path - strPath = '/home/pi/Desktop/'
strName = 'pi_enigma' #Preset document name
strPin = '5468295424' #Preset Pin is 10 digits long
setImgMode = 0# 0 = writes png image  : 1 = writes png image  : 2 = writes png image  : 3 = (RGBA writes to string -Encoding_Algorithm- not as good as png)
footNote = ''#'Footnote_Empty!' NOTE!! not encrypted!
strFn2 = 'Preset footnote number 2'#Press Right-ALT Preset footnote number 2 (up to 45 Characters)
#Default_System_Settings--------1
prefix = ':#:-' #Preset Unique prefix a (Sys watermark/User-Group/Department-ID)
sysPin = '5468295424' #System Pin is 10 digits long
preKey = 'keyCode'#Preset System Key/Password = keyCode
BgImgPath = 'Settings/Bg0.png' #Background image 0 file name
BgImgPath1 =  'Settings/Bg1.png'#Background image 1 file name
sysImgMode = 2#Must be set to 2 or 3
imgNo = 0 #Use image number
osName = 'Pi=4'#Pi model or os name ie. Pi3/Pi4/PiTop or Jessie/Buster/ect
useZ = True#pin algorithm use offsetZ
crptMode = 0#
#End----------------------------

strUID = ''#strUIDd #Your name or user ID
strGID = ''#strGIDd #The Name of your group
strPWD = ''#strPWDd #Password
strNewUID = ''
strNewGID = ''
strNewPWD = ''
strPF = ''
logonNo = 0
imgMode = 0
scrMode = 3 #Start up screen mode
genList = False
sysSave = False

#List of users User name-  Password  - Public-key will be encrypted
List_Users = []
#Font list 0 and font list 1
fontList0 = ['Carlito', 'Dingbats', 'FreeMono', 'FreeSans', 'FreeSerif', 'Gentium', 'Inconsolata', 'Lato', 'Monospace', 'msbm10']#Font list 0
#fontList0 = ['dejavuserif', 'dejavusansmono', 'dejavusans', 'Gentium', 'Inconsolata', 'Lato', 'Monospace', 'msbm10', 'FreeMono', 'FreeSans']

List_Char = ['_','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','u','r','s','t','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','U','R','S','T','V','W','X','Y','Z',
            '0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','+',':','|','<','>','\\','/','[',']',',','.','?']

List_List = [['+'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'],
             ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'],
             ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z'],
             ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'],
             ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z']]

List_Nums = []
List_Code = []

keyList = []
imgPathList = []

try:
    imgImg0 = pygame.image.load(BgImgPath1).convert()#BgImgPath
    imgImg1 = pygame.transform.scale(imgImg0, (SCREEN_WIDTH, SCREEN_HEIGHT))
    imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))
    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    offsetX = -int((sizeX - SCREEN_WIDTH) / 2)
    offsetY = -int((sizeY - SCREEN_HEIGHT) / 2)    
    
except:
    print('Error_:_Must_have_a_background_Image!!(' + BgImgPath1 + ')')
    pygame.quit()
    sys.exit()    

strData = ''
strLine0 = ''
strLine1 = 'Enter_System_Password/Empty=Preset_Password|F1=Help'#'Generate_Encoding_Algorithm!'
strLine2 = '**********'
strLine3 = ''
strLine4 = ''
strLine5 = ''
strLine6 = ''
strLine7 = ''
strLine8 = ''#Decode incoming message
strLine9 = ''
strLine10 = ''
strLine11 = ''
strLine12 = ''#Update_me!'#Disp buffer string

dspLine0 = ''
dspLine1 = ''
dspLine2 = ''
dspLine3 = ''
dspLine4 = ''
dspLine5 = ''
dspLine6 = ''
dspLine7 = ''
dspLine8 = ''
dspLine9 = ''

strUIDd = '' 
strGIDd = ''
strPWDd = ''

showPin = 0
showPass = 0
docNum = 0
charNum = 0
charM = '_'#Mouse type char
strNum = ''
rectAddY = 0
fontTyp = fontList0[0]
fontRot = 15
fontScl = 35

font0 = pygame.font.SysFont(fontTyp, fontScl)
font1 = pygame.font.SysFont('Courier', 16)#'FreeMono'

rectPosX = 250
rectPosY = 200
rectSizeX = 240
rectSizeY = 240

offsetX = 0
offsetY = 0
offsetZ = 0
inputNo = 0
dummyCount = 0


#======================================================================


def Encode0(strData):#GenCodeList
        
    global List_Code
    global strLine1
    
    goodImg = True

    List_Code.clear()
    List_Code = copy.deepcopy(List_List)

    for i in range(len(List_Code)):
    
        char = List_Code[i][0]
    
        for j in range(len(strData)):
        
            if (char == strData[j]):
                sublist = List_Code[i]
                sublist.append(j)
     
    for i in range(len(List_Code)):
        
        if (len(List_Code[i]) < 500):
            goodImg = False
  
    if (goodImg == False):
        strLine1 = 'Warning!_:_Image_Not_Suitable!'
        DrawScreen1()
        pygame.display.flip()
        time.sleep(4)

            
def Encode1(strMain):#Encode string
    
    for i in range(len(strMain)):
        char = strMain[i]
        if (genJunk):
            char = char.capitalize()
            Encode2(char)
            rndC = random.randrange(1, 5)
            for i in range(rndC):
                Encode2('~')
        else:
            Encode3(char)
            
def Encode2(char):#CharFilterIn

    #Filter char
    if (char == '~'):
        char = 'a'
    elif (char == '!'):
        char = 'b'
    elif (char == '@'):
        char = 'c'
    elif (char == '#'):
        char = 'd'
    elif (char == '$'):
        char = 'e'        
    elif (char == '%'):
        char = 'f'
    elif (char == '^'):
        char = 'g'
    elif (char == '&'):
        char = 'h'
    elif (char == '*'):
        char = 'i'         
    elif (char == '('):
        char = 'j'
    elif (char == ')'):
        char = 'k'
    elif (char == '-'):
        char = 'l'
    elif (char == '+'):
        char = 'm'         
    elif (char == '='):
        char = 'n'
    elif (char == '`'):
        char = 'o'
    elif (char == '|'):
        char = 'p'
    elif (char == '<'):
        char = 'q'         
    elif (char == '>'):
        char = 'u'
    elif (char == ']'):# Or }
        char = 'r'
    elif (char == '['):# Or {
        char = 's'
    elif (char == '\\'):
        char = 't'           
    elif (char == '.'):
        char = 'v'
    elif (char == ','):
        char = 'w'
    elif (char == '\''):
        char = 'x'
    elif (char == ':'):# Or ;
        char = 'y'         
    elif (char == '?'):
        char = 'z'
    elif (char == '_' or char == ' '):
        char = '+'
       
    Encode3(char)
    
               
def Encode3(char):#Encode char to number list
    
    for i in range(0, len(List_Code)):
        if (char == List_Code[i][0]):
            break
        
    rndC = random.randrange(1, len(List_Code[i]))
    codeNum = str(List_Code[i][rndC])
    List_Nums.append(codeNum)
  
 
#======================================================================

def Decode0(numList):#Decode Char from number list
  
    global strLine1
    global strLine8
    global strLine10
    global dummyCount
    
    strLine8 = ''
    strLine1 = ''
    
    try:
        for i in range(len(numList)):
            try:
                num = int(numList[i])
                char = strData[num]
                if (genJunk):
                    Decode1(char)
                else:
                    strLine8 += char
            except:
                strLine1 = str(numList[i])
    except:
        strLine1 = 'ERROR_:_Decode0_:_Problem!'
        print(strLine1)

    if (strLine1 == '{}'):
        strLine10 = '{There_is_no_footnote!}'
    else:
        strLine10 = strLine1
    
    if (len(strLine8) > dummyCount and genJunk):#dummyCount != 0):
        strLine1 = 'ERROR:[PIN/User/Key/Image/Image-Mode/OS-Version]'#-Incorrect!'
        UpdateDspMsg(strLine8, '')
    else:
        if (genJunk):
            strLine1 = 'Decoded!'
            UpdateDspMsg(strLine8, '')
        else:
            strLine1 = 'Enter=Next(to_Continue)|TAB=Back|ESC=Quit|F1=Help'
            if (showImg == False):
                UpdateDspMsg(strLine8, '')


def Decode1(char):#CharFilterOut   
  
    global strLine8
    global dummyCount

    if (char == 'a'):#Empty char dummy
        dummyCount += 1
        char = ''
    elif (char == 'b'):
        char = '!'
    elif (char == 'c'):
        char = '@'
    elif (char == 'd'):
        char = '#'
    elif (char == 'e'):
        char = '$'        
    elif (char == 'f'):
        char = '%'
    elif (char == 'g'):
        char = '^'
    elif (char == 'h'):
        char = '&'
    elif (char == 'i'):
        char = '*'         
    elif (char == 'j'):
        char = '('
    elif (char == 'k'):
        char = ')'
    elif (char == 'l'):
        char = '-'
    elif (char == 'm'):
        char = '+'         
    elif (char == 'n'):
        char = '='
    elif (char == 'o'):
        char = '`'
    elif (char == 'p'):
        char = '|'
    elif (char == 'q'):
        char = '<'         
    elif (char == 'u'):
        char = '>'
    elif (char == 'r'):
        char = ']' # Or }
    elif (char == 's'):
        char = '[' # Or {
    elif (char == 't'):
        char = '\\'           
    elif (char == 'v'):
        char = '.'
    elif (char == 'w'):
        char = ','
    elif (char == 'x'):
        char = '\''
    elif (char == 'y'):
        char = ':' # Or ;        
    elif (char == 'z'):
        char = '?'
    elif (char == '+'):
        char = '_'
        
    strLine8 += char

#======================================================================

def ReadFile0():#Read encoded file
    
    global strLine1
    global dummyCount
    global imgMode
    global crptMode
    global imgMode
    global imgNo
    
    dummyCount = 0
    crptMode = 0
    imgNo = 0
    imgMode = 0
    objFile = ''
    strNew = ''
    strMeta = ''
    proceed = False
    
    try:
        f = open(strPath + strName + strNum + '.txt', "r")
        if f.mode == 'r':
            objFile = f.read()                  
            f.close()
            proceed = True
    except:#
        strLine1 = 'ERROR_:_Could_Not_Find_File!' + strPath + strLine5 + '.txt'
        #print(strLine1)
        
    for i in range(len(objFile)):
        if(objFile[i] != '\n'):
            strNew += objFile[i]

    if (proceed):
        
        if (genJunk):
            
            crptMode = 3
            num = 0
            
            for i in range(len(strNew) - 1):
                search = strNew[i] + strNew[i+1]
                if (search != '] '):
                    strMeta += strNew[i]
                else:
                    num = i + 2
                    break

            strNew = strNew[num:]

            if (strMeta[0]  == '*'):#imgMode 0
                crptMode = 0
            elif (strMeta[0]  == ' '):#imgMode 1
                crptMode = 1
            elif (strMeta[0]  == '&'):#imgMode 2
                crptMode = 2
            else:
                print('Over-ride_:_old-version')
                imgMode = setImgMode
                imgNo = 0
     
            if (crptMode < 3):      
                if (useImgName):
                    imgMode = int(strMeta[1])
                    imgNo = int(strMeta[2])
                    strMeta = strMeta[4:]
                    strMeta = strMeta
                    #print('Image_Name_:_', strMeta)
                    try:    
                        if (len(imgPathList) > 0):
                            for i in range(len(imgPathList)):
                                if (imgPathList[i] == strMeta):
                                    imgNo = i     
                        else:
                            print('ERROR_:_No_Images!')        
                    except:
                        print('ERROR!')
        
                    #print('Image_No_:_', imgNo)   
                    
                else:
                    imgMode = int(strMeta[1])
                    imgNo = int(strMeta[2])
                    strMeta = strMeta[4:]
                    print('Image_Number_:_', imgNo)

        if (crptMode == 0 or genJunk == False):
            objFile = strNew

        elif (crptMode == 1):
            num = 10 + int(strPin[5]) + int(strPin[6]) + int(strPin[7])
            for c in strNew:
                x = ord(c)
                x = x - num
                c2 = chr(x)
                objFile = objFile + c2
            
        elif (crptMode == 2):
            pass
        
        else:
            print('ERROR_:_ReadFile-Out_Of_Range')
            
        if (imgMode == 1):
            if (useImgName):
                UpdateImage(imgPathList[imgNo])
                #print(imgPathList[imgNo])
            else:
                print('Use image file from name')

        if (scrMode != 3):
            UpdatePIN(strPin, strKey)

        listMain = objFile.split('~')
        Decode0(listMain)
        
    listMain.clear()
       
        
def CheckForFile(canI):
    
    global strLine1
    
    try:
        f = open(strPath + strName + strNum + '.txt', "r") 
        f.close()
        
        strLine1 = 'WARNING_:_(' + strName + strNum + '.txt)_Already_Exists!'
        #print('WARNING_Do_You_Want_To_Overwrite_This_File?_:_' + strNum + '.txt')
        canI = False
        
    except:
        canI = True
        #print('No such file! Go Ahead Make My Day!!')

    return (canI)


def WriteFile0(content):#Write encoded file 
    #print(content)
    global strLine1
    global crptMode
    global imgMode
    
    strNew = ''
    
    try:#Test to see if Folder Ex
        os.mkdir(strPath)
        strLine1 = 'WriteFile0_:_Made_New_Folder!_>_' + strPath
        #print('WriteFile0_:_Made_New_Folder!_>_' + strPath)
    except:
        pass

    content = '~'.join(content)
    content += '~{' + footNote + '}'  

    if (genJunk):
        
        if (useImgName and imgMode != 0 and imgMode != 4):
            imgName = strPF
        else:
            imgName = 'NONE'
        
        if (crptMode == 0):
            content = '*' + str(imgMode) + str(imgNo) + '[' + imgName + '] ' + content
            
        elif (crptMode == 1):
            num = 10 + int(strPin[5]) + int(strPin[6]) + int(strPin[7])
            for c in content:
                x = ord(c)
                x = x + num
                c2 = chr(x)
                strNew = strNew + c2
                
            content = ' ' + str(imgMode) + str(imgNo) + '[' + imgName + '] ' + strNew
            strNew = ''
            
        elif (crptMode == 2):
            content = '&' + str(imgMode) + str(imgNo) + '[' + imgName + '] '  + content                  
           
    for i in range(len(content)):
        if (i % 80 == 0 and i > 1):
            strNew += '\n'
        strNew += content[i]
    
    try:
        f = open(strPath + strName + strNum + '.txt', "w")
        f.write(strNew)#\n
        f.close()
 
    except IOError:
        strLine1 = 'ERROR_:_Could_Not_Create_File!'
        print('ERROR_:_Could_Not_Create_File!')
    
    crptMode = 0
    content = ''
    strNew = ''
    List_Nums.clear()

def WriteImage():#create public image
    
    global strLine1
    strLine1 = 'Writing_Image_To_Folder!_>_' + strPath
    DrawScreen1()
    pygame.display.flip()
    
    try:#Test to see if Folder Ex
        os.mkdir(strPath)
        strLine1 = 'WriteFile0_:_Made_New_Folder!_>_' + strPath
        #print(strLine1)
    except:
        pass
    
    try:
        imgImg = pygame.image.load(imgPathList[imgNo])
        strP = strPath + strName + strNum + '.png'
        pygame.image.save(imgImg, (strPath + strName + strNum + '.png'))#'Images/image.png'
        strLine1 = 'Image_Path_:_' + strP
        #print('Image_Path_:_' + strP)
    except:
        strLine1 = 'ERROR_:_Could_Not_Save_Image_To_Folder!'
        print('ERROR_:_imgMode_:_Could_Not_Save_Image_To_Folder!')

def UpdatePIN(pin, strKey):#PIN and Key

    global hudStr7
    global hudStr8
    global hudStr9
    global strLine1
    global font0
    global rectPosX
    global rectPosY 
    global rectSizeX 
    global rectSizeY
    global offsetZ
    global strPF

    keyList.clear()
    offsetZ = 0
    
    if (imgMode != 2 and imgMode != 3):
        
        try:
            R = int(pin[2]) * 2 * int(pin[3]) + 25 + int(pin[5]) #print(R)
            B = int(pin[0]) * 2 * int(pin[7]) + 25 + int(pin[9]) #print(B) 
            G = int(pin[1]) * 2 * int(pin[6]) + 25 + int(pin[3]) #print(G)
            offsetZ = int(pin[int(pin[1])]) + (int(pin[int(pin[6])]) * 10) + (int(pin[int(pin[3])]) * 100)
            
            fontTyp0 = fontList0[int(pin[5])]#Font type you can swop out PIN's 0-9
            fontTyp1 = fontList0[int(pin[1])]#Font type you can swop out PIN's 0-9
            fontTyp2 = fontList0[int(pin[9])]#Font type you can swop out PIN's 0-9
            fontRot = (15 * int(pin[2]))#Rotate font you can swop out PIN's 0-9
            fontScl0 = ((int(pin[3]) + int(pin[5])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl1 = ((int(pin[4]) + int(pin[8])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl2 = ((int(pin[4]) + int(pin[6])) + 12)#Scale font you can swop out PIN's 0-9

            newPWD0, newUID = UserSearch(strUID, '', 0)#
            if (newUID == ''):
                newUID = strUID

            newPWD1, newKey = UserSearch(strKey, '', 0)#
            if (newKey == ''):
                newKey = strKey

            if (strKey == strGID):
                keyList.append(newKey)
                keyList.append(newKey)
            else:
                keyList.append(newKey)
                keyList.append(newUID)                
                    
            #Make it easer for listed and non listed encode/decode        
            if (logonNo != 4 or strKey == newKey):
                strLine1 = 'Warning:_User/Sender_Not_in_list!'
                
                if (1 == 1):#Show warning
                    #print(strLine1)
                    DrawScreen1()
                    pygame.display.flip()
                    time.sleep(4)
                
                keyList.clear()
                keyList.append(strUID)
                keyList.append(strKey)

            keyList.sort(key = lambda keyList: keyList)

            font0 = pygame.font.SysFont(fontTyp0, fontScl0)
            hudStr7 = font0.render(keyList[0] + prefix, True, (G,R,B))#R,G,B
            hudStr7 = pygame.transform.rotate(hudStr7, fontRot)
            
            font1 = pygame.font.SysFont(fontTyp1, fontScl1)
            hudStr8 = font1.render(prefix + keyList[1], True, (R,B,G))
            hudStr8 = pygame.transform.rotate(hudStr8, fontRot) 

            font2 = pygame.font.SysFont(fontTyp2, fontScl1)
            hudStr9 = font1.render(prefix + sysKey, True, (B,G,R))
            hudStr9 = pygame.transform.rotate(hudStr9, fontRot)
            
            rectPosX = (int(pin[4]) * int(pin[5])) * 5 + 15
            rectPosY = (int(pin[5]) * int(pin[3])) * 3 + 10
            rectSizeX = (int(pin[6]) * 10) + 240
            rectSizeY = (int(pin[7]) * 10) + 240
            
            #Image offset
            eOffsetX = offsetX - int(pin[8]) * 10  
            eOffsetY = offsetY - int(pin[9]) * 10
                
            scaleAddXY = int(pin[5]) + int(pin[6])
            
            if (int(pin[3]) + int(pin[7]) % 2 == 0):
                rotation = 0  
            else:
                rotation = 180
        except:
            strLine1 = 'ERROR_:_UpdatePIN-PIN_Mode_0'
            print(strLine1)
        
    else:#Image mode 2 Png Password mode & 3 is RGB Password mode 

        try:
            R = int(pin[0]) * 2 * int(pin[7]) + 25 + int(pin[9]) #print(B) 
            B = int(pin[1]) * 2 * int(pin[6]) + 25 + int(pin[3]) #print(G)
            G = int(pin[2]) * 2 * int(pin[3]) + 25 + int(pin[5]) #print(R)
            offsetZ = int(pin[int(pin[2])]) + (int(pin[int(pin[5])]) * 10) + (int(pin[int(pin[7])]) * 100)
            
            fontRot = (15 * int(pin[2]))#Rotate font you can swop out PIN's 0-9
            
            fontTyp0 = fontList0[int(pin[1])]#Font type you can swop out PIN's 0-9
            fontTyp1 = fontList0[int(pin[7])]#Font type you can swop out PIN's 0-9
            fontTyp2 = fontList0[int(pin[8])]#Font type you can swop out PIN's 0-9            
            fontScl0 = ((int(pin[3]) + int(pin[5])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl1 = ((int(pin[4]) + int(pin[1])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl2 = ((int(pin[7]) + int(pin[8])) + 12)#Scale font you can swop out PIN's 0-9
            
            font0 = pygame.font.SysFont(fontTyp0, fontScl0)
            hudStr7 = font0.render(strKey + prefix, True, (G,R,B))#R,G,B
            hudStr7 = pygame.transform.rotate(hudStr7, fontRot)
             
            font1 = pygame.font.SysFont(fontTyp1, fontScl1)
            hudStr8 = font1.render(prefix + strKey, True, (R,G,B))# + strName prefix +    
            hudStr8 = pygame.transform.rotate(hudStr8, fontRot)

            font2 = pygame.font.SysFont(fontTyp2, fontScl1)
            hudStr9 = font1.render(prefix + sysKey, True, (B,G,R))
            hudStr9 = pygame.transform.rotate(hudStr9, fontRot)
            
            rectPosX = (int(pin[4]) * int(pin[5])) * 5 + 15
            rectPosY = (int(pin[5]) * int(pin[3])) * 3 + 10
            rectSizeX = (int(pin[6]) * 10) + 240
            rectSizeY = (int(pin[7]) * 10) + 240
            
            #Image offset
            eOffsetX = offsetX - int(pin[8]) * 10  
            eOffsetY = offsetY - int(pin[9]) * 10
                
            scaleAddXY = int(pin[3]) + int(pin[7])
            
            if (int(pin[4]) + int(pin[8]) % 2 == 0):
                rotation = 0  
            else:
                rotation = 180
                
        except:
            strLine1 = 'ERROR_:_UpdatePIN-PIN_Mode_1'
            print(strLine1)

    if (genJunk):
        if (imgMode == 0):
            strPF = strPath + strName + '.png'        
        elif (imgMode == 4):
            strPF = 'Settings/.selfGenImg.png'
            SelfGenImg(strPF, pin)
        else:
            strPF = imgPathList[imgNo]
            
    else:
        strPF = BgImgPath1
    #print(strPF)           
    GenImage(strPF, eOffsetX, eOffsetY, rotation, scaleAddXY)
    keyList.clear()

def SelfGenImg(strPF, pin0):#Back screen
    
    try:
        R = int(pin0[2]) * 2 * int(pin0[3]) + 25 + int(pin0[8]) #print(R)
        B = int(pin0[0]) * 2 * int(pin0[7]) + 25 + int(pin0[6]) #print(B) 
        G = int(pin0[1]) * 2 * int(pin0[6]) + 25 + int(pin0[2]) #print(G)
        A = int(pin0[3]) * 2 * int(pin0[5]) + 25 + int(pin0[9]) #print(A)
        
        colorList = [(R,G,B),(B,G,R),(R,A,R),(B,G,B),(G,G,B),(A,R,B),(B,G,R),(B,B,B),(R,G,G),(B,A,B)]
        
    except:
        print('ERROR_:_SelfGenImg!')

    screen.fill(colorList[int(pin0[9])])
    
    rad = 15
    loopNo = int(pin0[5])
    posY = 0
    for i in range(12):
        posX = 0
        for j in range(16):
            if (loopNo < 9):
                loopNo += 1
            else:
                loopNo = 0
            val = int(pin0[loopNo])
            pygame.draw.rect(screen, colorList[val], pygame.Rect(posX, posY, 100, 100), val) 
            posX += 50
            
        posY += 50
        
    loopNo = int(pin0[8])
    center = int(SCREEN_WIDTH * .5), int(SCREEN_HEIGHT * 0.5)
    for i in range(32):
        
        if (loopNo < 9):
            loopNo += 1
        else:
            loopNo = 0
        val = int(pin0[loopNo])
        if (val == 0):
            val = 1
        
        pygame.draw.circle(screen, colorList[val], center, rad, val)
        rad += 15
        
    try:
        rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)#PosX, PosY, RecSizeX, RecSizeY
        sub = screen.subsurface(rect)
        sub = pygame.transform.scale(sub, (1040, 780)) 
        pygame.image.save(sub, strPF)
        pygame.image.save(sub, 'Images/SelfGen.png')
        
    except:
        print('ERROR_:_Sub-Rescale_Or_Save!')
   
    if (debug):
        pygame.display.flip() 
        time.sleep(5)

    
def UpdateImgList():
    
    global imgCount
    global imgPathList
    
    try:
        imgPathList.clear()
        imgPathList = glob.glob('Images/*')
        #print(imgPathList)
        if (len(imgPathList) > 0):
            c = 0
            for i in range(len(imgPathList)):
                if (imgPathList[i] == BgImgPath):
                    c = int(i)   
                    imgPathList.remove(imgPathList[c])
        else:
            print('ERROR_:_No_Images!')

    except:
        print('ERROR_:_No_Images!')
        imgPathList = [BgImgPath]
    
    imgCount = len(imgPathList) - 1
    

def UpdateImage(filePath):

    global imgImg0
    global imgDsp0 
    global strLine1
    
    try:
        imgImg0 = pygame.image.load(filePath).convert()
        imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))  
    except:
        strLine1 = 'ERROR_:_Missing_File!_' + filePath
        #print(strLine1)
        DrawScreen1()
        pygame.display.flip()        
        time.sleep(5)
        imgImg0 = pygame.image.load(BgImgPath).convert()
        imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))
        
             
def GenImage(fileName, eOffsetX, eOffsetY, rotation, scaleAddXY):

    global imgImg0
    global strLine1

    List_Nums.clear()
    
    UpdateImage(fileName)
    
    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    
    if (sizeX < 960 or sizeY < 720):
        if (genJunk):
            strLine1 = 'ERROR_:_GenImage-Image_Was_Rescaled!'
            print(strLine1)
        imgImg0 = pygame.transform.scale(imgImg0, (1000, 800))      
        
    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    offsetX = -int((sizeX - SCREEN_WIDTH) / 2)
    offsetY = -int((sizeY - SCREEN_HEIGHT) / 2)
    
    offsetX += eOffsetX
    offsetY += eOffsetY
    
    imgImg0 = pygame.transform.rotate(imgImg0, rotation)
    imgImg0 = pygame.transform.scale(imgImg0, (sizeX + scaleAddXY, sizeY + scaleAddXY)) 
        
    DrawScreen0(1)
    
    try:
        rect = pygame.Rect(rectPosX, rectPosY, rectSizeX, rectSizeY)#PosX, PosY, RecSizeX, RecSizeY
        sub = screen.subsurface(rect)
        
        if (imgMode < 3):
            pygame.image.save(sub, BgImgPath)#'Images/image.png'
        else:
            data = pygame.image.tostring(sub, 'RGB')#RGBA_PREMULT RGBX 
            
    except:
        strLine1 = 'ERROR_:_GenImage-Subsurface_Rectangle_Outside_Surface_Area!'
        print('ERROR_:_GenImage-Subsurface_Rectangle_Outside_Surface_Area!')
       
    DrawScreen0(0)
    strLine1 = 'Generating_Encoding_Algorithm!'
    #print(strLine1)
    DrawScreen1()
    pygame.display.flip()

    if (imgMode != 3):
        GetImage(BgImgPath)#image
    else:
        GetString(data)
        data = ''

def GetString(data):

    global strData
    global strLine1
    
    strData = ''
    
    try:
        encodingStr = base64.b64encode(data)
        strData = str(encodingStr, "utf-8") + '=='
        data = ''     
        
    except:
        print('Error_:_GetString!')
        
    Encode0(strData)

    
def GetImage(fileName):#Incode image from file and send it

    global strData
    global strLine1
    
    strData = ''
    
    try:
        with open(fileName, 'rb') as imageFile:
            encodingStr = base64.b64encode(imageFile.read())
            strData = str(encodingStr, "utf-8") + '=='
            #print('Got_Image - ' + fileName )
    except:
        strLine1 = 'ERROR_:_Could_Not_Find_File_-GetImage-!'
        print('ERROR_:_Could_Not_Find_File_-GetImage-!')
    
    try:
        pygame.image.save(imgImg1, fileName)#Overite image
        #os.remove(fileName)#Remove image

    except:
        strLine1 = 'ERROR_:_Could_Not_Removed_File_:_' + 'Images/' + fileName + '.png'
        print('ERROR_:_Could_Not_Removed_File_:_' + 'Images/' + fileName + '.png')
    
    if (offsetZ > 0 and useZ and len(strData) > 50000):
        strData = strData[offsetZ:]
        #print('UseZ',useZ,'_:_',len(strData),'_:_',offsetZ)
    Encode0(strData)
    
    try:
        if (imgMode == 4):
            os.remove('Settings/.selfGenImg.png')#Remove self gen-image
    except:
        print('ERROR:_GetImage!_Image-Mode')

def Reset():
    
    global footNote
    global strLine0
    global strLine1
    global strLine3
    global strLine8 
    global strLine12
    global inputNo
    global imgMode
    
    imgMode = setImgMode
    footNote = ''
    strLine0 = ''
    strLine3 = ''
    strLine8 = ''
    strLine12 = ''
    inputNo = 0
    strLine1 = 'Reset!'
    UpdateDspMsg('', '')
    UpdateImgList()


#==============================================================================

def KMInput():
 
    global strLine0
    global strLine1
    global strLine3
    global charM
    global charNum
    global scrMode
    global setImgMode
    global docNum
    global strNum
    global inputNo
    global logonNo
    global conDel
    global genList
    global BZLCOL 
    
    useKey = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif (event.type == pygame.KEYDOWN):
            
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                UpdateEnter()
                useKey = False
                
            elif (event.key == pygame.K_LCTRL):
                UpdateCTRL(0)
                useKey = False
                
            elif (event.key == pygame.K_RCTRL):
                UpdateCTRL(1)
                useKey = False
            
            elif (event.key == pygame.K_DELETE):
                if (logonNo == 11):
                    if (conDel == False and strUID != strUIDd):
                        strLine1 = 'DEL=CANCEL_DELETE_USER|ENTER=Delete&Exit'
                        conDel = True
                    else:
                        if (strUID != strUIDd):
                            strLine1 = 'DEL=Delete_User|ENTER=Exit'
                        else:
                            strLine1 = 'ERROR:No_Can_Do!|L-ALT=PREV|R-ALT=NEXT'
                            
                        conDel = False 
                else:
                    strLine0 = ''
                    strLine1 = 'Deleted_Line/Message!'
                    docNum = 0
                    strNum = ''
                
            elif (event.key == pygame.K_LALT):
                UpdateAlt(0)
                    
            elif (event.key == pygame.K_RALT):
                UpdateAlt(1)

            elif (event.key == pygame.K_TAB):
                UpdateTab(0)
                
            elif (event.key == pygame.K_F1):
                UpdateF1()
                useKey = False
                
            elif (event.key == pygame.K_F2):
                UpdateF2(0)
                useKey = False
                
            elif (event.key == pygame.K_F10):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(1)#1 = Goto ADD user mode
                useKey = False
                
            elif (event.key == pygame.K_F11):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(2)#2 = Goto EDIT user mode
                    UpdateEdit(0)
                useKey = False

            elif (event.key == pygame.K_F12):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(3)#3 = Goto DELETE user mode
                    UpdateEdit(0)
                elif (scrMode == 3):
                    if (genList == False):
                        genList = True
                        strLine1 = 'New_Key+ENTER=New/OverWrite_User_List|F12=Cancel'
                    else:
                        genList = False
                        strLine1 = 'ENTER=Logon_To_System|ESC=Quit|F1=Help'

                useKey = False
                
            elif (event.key == pygame.K_ESCAPE):
                
                if (inputNo != 0):
                    Reset()
                else:
                    if (scrMode == 1 or scrMode == 2):
                        scrMode = 0
                        logonNo = 0
                        setImgMode = 0
                        strLine1 = 'Enter=Next/ESC=Return_To_System_Screen'
                        
                    elif (scrMode == 3):
                         scrMode = -1

                    elif (scrMode == 0):
                        if (logonNo != 0):
                            ClearSubWin()
                            logonNo = 0
                        else:
                            BZLCOL = RED
                            strLine1 = 'Enter=Next/ESC=Quit'
                            scrMode = 3
                
                useKey = False
                    
            elif event.key == pygame.K_BACKSPACE:
                if (len(strLine0)>0):
                    strLine0 = strLine0[:-1]
                else:
                    if (inputNo != 0):
                        UpdateTab(0)#inputNo
                        useKey = False
            else:
                if (event.unicode != '~'):
                    if (inputNo == 5 and genJunk):
                        strLine0 += event.unicode.capitalize() 
                    else:
                        strLine0 += event.unicode              

            if (useKey):
                charNum = 0
                charM = '_'
                UpdateChar(strLine0, charM)  
            
        #Mouse input
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]#
        
        if (event.type == pygame.MOUSEBUTTONDOWN):
            
            if event.button == LEFT:#Left click
                    UpdateEnter()
                    
            elif event.button == MIDDLE:# Middle click
                if (inputNo == 0 and logonNo > 2):#if (logonNo > 2):
                    if (scrMode != 0):
                        scrMode = 0
                    else:
                        scrMode -= 1
                else:
                    charNum = 0
                    strLine0 += charM
                    UpdateChar(strLine0, charM)
                    charM = '_'
                    UpdateChar(strLine0, charM)

            elif event.button == RIGHT:#Right click
                if (len(strLine0)>0):
                    strLine0 = strLine0[:-1]
                else:
                    if (inputNo == 0 or inputNo ==1):
                        if (scrMode != 3):
                            UpdateCTRL(0)
                    else:
                        UpdateTab(0)#inputNo
                        
                UpdateChar(strLine0, charM)
      
            elif event.button == UP:# Wheel Up
                
                if (inputNo == 0 and logonNo > 2):
                        UpdateAlt(1)
                        
                elif (inputNo == 1):
                    charM = str(charNum)
                    if (charNum < 9):
                        charNum += 1
                    else:
                        charNum = 0
                else:
                    if (charNum < len(List_Char) - 1):
                        charNum += 1
                    else:
                        charNum = 0
                        
                    charM = List_Char[charNum]
                    
                if (inputNo == 5 and genJunk):
                    charM = charM.capitalize()                     
                UpdateChar(strLine0, charM)
                
            elif event.button == DOWN:# Wheel Down
                
                if (inputNo == 0 and logonNo > 2):
                    UpdateAlt(0) 
                    
                elif (inputNo == 1):
                    charM = str(charNum)
                    if (charNum > 1):
                        charNum -= 1
                    else:
                        charNum = 9
                else:
                    if (charNum > 0):
                        charNum -= 1
                    else:
                        charNum = len(List_Char) - 1
                        
                    charM = List_Char[charNum]
                        
                if (inputNo == 5 and genJunk):
                    charM = charM.capitalize() 
                UpdateChar(strLine0, charM)                          


def UpdateChar(strLine, charA):
    
    global strLine0 
    global strLine1
    global strLine2
    global strLine3
    global strLine4
    global strLine5
    global strLine6
    global strLine10
    global rectAddY
    global iCan
    global strUIDd
    global strGIDd
    global strPWDd
    

    if (inputNo == 0):

        if (len(strLine) > 19):
            strLine0 = strLine0[:-1]
        
        if (logonNo == 0 or logonNo == 5 or scrMode == 3 ):
            if (scrMode == 3):
                if (showPass == 0):
                    strPWDd = ''
                    n = int(len(strLine))
                    for i in range(n):
                        strPWDd += '*'
                    strPWDd += '[' + charA + ']'
                else:
                    strPWDd = strLine + '[' + charA + ']'# + '_=_' + str(len(strLine0))                       
            else:
                strUIDd = strLine + '[' + charA + ']'
            
        elif (logonNo == 1 or logonNo == 6 or logonNo == 9):
            strGIDd = strLine + '[' + charA + ']'
        
        elif (logonNo == 2 or logonNo == 7 or logonNo == 10):
            
            if (showPin == 0):
                strPWDd = ''
                n = int(len(strLine))
                for i in range(n):
                    strPWDd += '*'
                strPWDd += '[' + charA + ']' #+ '_=_' + str(n)
            else:
                strPWDd = strLine + '[' + charA + ']'# + '_=_' + str(len(strLine0))           
            
    elif (inputNo == 1):
        
        if (showPin == 0):
            strLine2 = ''
            n = int(len(strLine))
            for i in range(n):
                strLine2 += '*'
            strLine2 += '[' + charA + ']' + '_=_' + str(n)
        else:
            strLine2 = strLine + '[' + charA + ']' + '_=_' + str(len(strLine0))
                    
    elif (inputNo == 2):
        
        if (showPass == 0):
            strLine3 = ''
            n = int(len(strLine))
            for i in range(n):
                strLine3 += '*'
            strLine3 += '[' + charA + ']' + '_=_' + str(n)
        else:
            strLine3 = strLine + '[' + charA + ']' + '_=_' + str(len(strLine0))
            
    elif (inputNo == 3):
        strLine4 = strLine  +  '/[' + charA + ']'
        iCan = False

    elif (inputNo == 4):
        strLine5 = strLine + strNum + '.txt[' + charA + ']'
        iCan = False

    elif (inputNo == 5):
        
        if (len(strLine) < 501): 
            strLine6 = strLine #+ '[' + charA + ']'
            a = int(len(strLine) / 50)
            totL = 50 - (len(strLine) - a * 50)
            totR = 500 - len(strLine)
            rectAddY = 20 * a
            if (totR != 0):
                strLine1 = 'Character\'s_left_in_Line=' + str(totL) + '_:_Total=' + str(totR)
            else:
                strLine1 = 'You_Have_No_Characters_Left_Over!'
        else:
            strLine0 = strLine0[:-1]
            strLine1 = 'You_Have_No_Characters_Left_Over!_It\'s_Full!!'

        UpdateDspMsg(strLine6, '[' + charA + ']')
               
    elif (inputNo == 6):
        
        if (len(strLine) < 46): 
            strLine10 = strLine + '[' + charA + ']'
            strLine1 = 'Footnote_NOT_Encrypted!|Character\'s_left_in_Line=' + str(45 - len(strLine))
        else:
            strLine0 = strLine0[:-1]
            strLine1 = 'ERROR_:_Footnote_to_Long'
            
def UpdateEnter():
    
    global strLine0
    global strLine1
    global strLine2
    global strLine3
    global strLine4
    global strLine5
    global strLine6
    global strLine7
    global strLine8
    global strLine9
    global strLine10
    global strLine12
    global footNote
    global charM 
    global strKey
    global strPin
    global inputNo
    global strPath
    global strName
    global docNum
    global charNum
    global canI
    global iCan
    global showPin
    global showPass
    global setImgMode
    global rectAddY
    global sysKey
    global scrMode
    global strPWDd
    global strLine3
    global imgMode
    
    strLine1 = 'None!'
    charNum = 0
    showPass = 0
    showPin = 0
    charM = '_'
    strPWDd = ''

    if (inputNo == 0):
        
        strLine1 = 'Enter=Next(to_Continue)|TAB=Back|ESC=Quit|F1=Help'
        
        if (scrMode == 0):
            UpdateUser(0)
            
        elif (scrMode == 3):
            if (strLine0 != ''):
                sysKey = strLine0
                if (genList):
                    LoadList(0)
                else:
                    LoadList(2)
            else:
                sysKey = preKey
                LoadList(1)
            strLine0 = ''
            scrMode = 0

        else:
            Reset()
            rectAddY = 0
            iCan = False
            strLine1 = 'Enter a 10 digit PIN/press Enter to ues preset PIN!'
            inputNo += 1
            strLine0 = ''          

    elif (inputNo == 1):#UpdatePin()
        
        if (strLine0 != ''):
            try:
                n = int(strLine0)
                if (len(strLine0) == 10):
                    strPin = strLine0
                    strLine2 = 'Updated_PIN!'
                    inputNo += 1
                    strLine0 = ''
                    
                else:
                    strLine1 = 'ERROR_:_PIN_Must_Be_10_Digits_Long_And_Not_(' + str(len(strLine0)) + ')!'
                    strLine0 = ''
                    strLine2 = ''
                    
            except:
                strLine1 = 'ERROR_:_PIN_Must_Only_Be_Numbers_And_10_Digits_Long!'
                strLine0 = ''
                strLine2 = ''

        else:
            strLine2 = 'Using_Preset_PIN!'
            strLine1 = 'Puplic_Key=Name/Key/Password_of_(Sender-Recever)'
            strKey = ''
            inputNo += 1
            
    elif (inputNo == 2):#UpdateKey()
        if (strLine0 != ''):
            strKey = strLine0
            if (imgMode != 0 and imgMode != 1 and imgMode != 4):
                UpdatePIN(strPin, strKey)
            strLine3 = 'Updated_Key!'
            strLine1 = 'Enter new Path/press Enter to use preset Path!'
            inputNo += 1
            strLine0 = ''            
        else:
            strLine1 = 'Puplic_Key=Name/Key/Password_of_(Sender-Recever)'

        
    elif (inputNo == 3):#Update File Path
        if (strLine0 != ''):
            strPath = strLine0 + '/'
            strLine4 = strPath
        else:
            strLine4 = strPath
            
        strLine1 = 'Enter a File-Name/press Enter to use preset Name!'
        inputNo += 1
        strLine0 = ''
    
    elif (inputNo == 4):#Update encoded file name
        if (strLine0 != ''):
            strName = strLine0
            strLine5 = strLine0 + strNum
        else:
            strLine5 = strName + strNum
            
        strLine1 = 'Type an Encrypted message/press Enter to read file!'
        inputNo += 1
        strLine0 = strLine12
        strLine9 = dspLine0
         
    elif (inputNo == 5):#Update message
        
        if (strLine0 != ''):
            
            a = int(len(strLine0) / 50)
            totL = 50 - (len(strLine0) - a * 50)
            
            if (totL < 50 and genJunk):
                for i in range(totL):
                    strLine0 += '_'
                    
            strLine1 = 'Press Enter To Encode or Type To Continue!'
            UpdateChar(strLine0, charM)

            if (totL == 50 or genJunk == False):
                strLine1 = 'Footnote (NOT ENCRYPTED!!)/press Enter To Continue!'
                strLine12 = strLine0
                strLine0 = footNote
                inputNo = 6 
                UpdateChar(footNote, '_')
        else:
        
            strLine1 = 'Decoded_:_' + strLine5 + '_:_Press_Enter_To_Continue!'
            ReadFile0()#Read coded file
            strLine7 = strLine8
            inputNo = 7
            
    elif (inputNo == 6):
        
        if (strLine0 != ''):
            footNote = strLine0
            
        canI = CheckForFile(canI)
                
        if (canI or iCan):
            
            imgMode = setImgMode

            if (imgMode == 0 or imgMode == 1 or imgMode == 4):
                
                if (imgMode == 0):# or imgMode == 1):
                    WriteImage()
                    
                UpdatePIN(strPin, strKey)
            
            if (genJunk):
                strAdd = ''
                rndC = random.randrange(1, 5)
                for i in range(rndC):
                    strAdd += '~'
                strLine12 = strAdd + strLine12
            Encode1(strLine12)#strLine6 strLine0
            strLine6 = ''
            WriteFile0(List_Nums)
            ReadFile0()
            inputNo = 7 
            strLine0 = strName # + str(docNum)
            strLine1 = 'Encoded_File_Name_:_' + strLine5 +'.txt'
            iCan = False
            
        else:   
            strLine0 = strPath # if inputNo = 3
            if (len(strLine0) > 0):
                strLine0 = strLine0[:-1]
            inputNo = 3
            iCan = True

    elif (inputNo == 7):#Result
        strLine1 = 'Enter new Path/press Enter to use preset Path!'
        strLine0 = ''# strName #
        strLine5 = strLine0
        
        if (imgMode != 0 and imgMode != 1 and imgMode != 4):
            inputNo = 3
        else:
            inputNo = 1
            
        footNote = ''
        strLine3 = ''
        strLine8 = ''
        strLine12 = ''
        iCan = False
        rectAddY = 0
        UpdateDspMsg('', '')


def UpdateCTRL(num):
    
    global scrMode
    global setImgMode
    global inputNo
    global strLine1
    global logonNo
    global editMode 
    global crptMode
    
    if (scrMode !=0 and scrMode != 3):
        if (inputNo == 0):
            
            if (num == 0):
                if (setImgMode > 1):
                    setImgMode -= 1
                else:
                    setImgMode = 4                
            else:
                if (setImgMode < 4):
                    setImgMode += 1
                else:
                    setImgMode = 0
            strLine1 = 'Image_Mode_:_' + str(setImgMode)
            
        elif (inputNo == 5 and len(strLine0) > 0):
            if (num == 0):
                crptMode = 0
                strLine1 = 'Duel_Crypto_Mode_Is_Off'
            else:
                crptMode = 1
                strLine1 = 'Duel_Crypto_Mode_Is_On'                
        else:
            strLine1 = 'CTRL_Has_No_Function_At_This_Time!'


def UpdateAlt(num):
    
    global docNum
    global imgNo
    global strNum
    global strLine0
    global strLine1
    global showPin
    global showPass
    
    aNum = 'N'
    bNum = 'N'
    cNum = 'N'
    
    if (num == 0):#Left ALT Key
        
        if (inputNo == 0):
            
            if (scrMode == 0):
                if (logonNo == 8 or logonNo == 11 and conDel == False):
                    UpdateEdit(2)            
            elif (scrMode == 1 or scrMode == 2):
                if (imgNo > 0):
                    imgNo -= 1
                else:
                    imgNo = imgCount

                strLine1 = 'No:' + str(imgNo) + '_:_Path:' + imgPathList[imgNo]
                UpdateImage(imgPathList[imgNo])
                
            elif (scrMode == 3):
                showPass = 0
  
        elif (inputNo == 1):
            showPin = 0
        
        elif (inputNo == 2):
            showPass = 0
            
        elif (inputNo == 4):
            
            if (docNum > 0):
                docNum -= 1
                strNum = str(docNum)
                
            if (docNum == 0):
                strNum = ''
                
            strLine1 = 'New_Document_Name_:_' + strLine0 + strNum

        elif (inputNo == 5):#Main encrypted message
            pass

                
        elif (inputNo == 6):#footnote
            
            if (strKey == strGID):
                strInfo = strGID
            else:
                strInfo = strUID
                
            if (BZLCOL == BLACK):#Logon system is true
                aNum = 'Y'
                
            if (logonNo == 4):#Logon user is true
                bNum = 'Y'

            if (useZ):#Use offsetZ is true
                cNum = 'Y'
                
            strLine0 = 'Key*=' + strInfo + '|Img-Mode=' + str(setImgMode) + ':' + str(crptMode) + '|Logon=' + aNum + bNum + cNum + '|' + osName

            UpdateChar(strLine0, '')
        
    else:#Right ALT Key

        if (inputNo == 0):

            if (scrMode == 0):
                if (logonNo == 8 or logonNo == 11 and conDel == False):
                    UpdateEdit(1)
                    
            elif (scrMode == 1 or scrMode == 2):         
                if (imgNo < imgCount):
                    imgNo += 1
                else:
                    imgNo = 0
             
                strLine1 = 'No:' + str(imgNo) + '_:_Path:' + imgPathList[imgNo]
                UpdateImage(imgPathList[imgNo])
                
            elif (scrMode == 3):
                showPass = 1    
        
        elif (inputNo == 1):
            #showPin = 1
            pass
        
        elif (inputNo == 2):
            showPass = 1
            
        elif (inputNo == 4):
            docNum += 1
            strNum = str(docNum)
            strLine1 = 'New_Document_Name_:_' + strLine0 + strNum
            
        elif (inputNo == 5):#Main encrypted message
            pass
                
        elif (inputNo == 6):#footnote
            strLine0 = strFn2
            UpdateChar(strLine0, '')

        
def UpdateTab(num):#inputNo
    
    global inputNo
    global strLine0
    global strLine12
    global logonNo
    
    if (inputNo == 5):
        strLine12 = strLine0
        
    strLine0 = ''
    
    if (inputNo == 6):
        strLine0 = strLine12
          
    if (inputNo != 0):
        if (num == 0):
                
            if (inputNo > 1):
                inputNo -= 1
            else:
                inputNo = 1
                
        else:
            if (inputNo < 6):
                inputNo += 1
            else:
                inputNo = 1               
    else:

        if (num == 0):
            
            if (logonNo != 11):
                if (logonNo != 0 and logonNo != 5 and logonNo != 8):
                    logonNo -= 1
                else:
                    logonNo += 2   
        else:
            if (logonNo < 2):
                logonNo += 1
            else:
                logonNo = 0
                

def UpdateF1():
    
    global strLine1
    
    if (inputNo == 0):
        if (logonNo == 0):
            if (scrMode == 3):
                strLine1 = 'F12=Create-Overwrite_(User-List)'
            else:
                strLine1 = 'User-Name_&_Password/Your_Public-Key_no_Password' 
        elif (logonNo == 1):
            strLine1 = 'Group-Name/Group_Public-Key/Leave_Empty=Auto-Fill' 
        elif (logonNo == 2):
            strLine1 = 'Password_&_Enter|Administrator-Enter/F10/F11/F12'
        elif (logonNo == 5):
            strLine1 = 'Add_A_New_User_Name|ENTER=Next|TAB=Back|ESC=Cancel'
        elif (logonNo == 6):
            strLine1 = 'Enter_A_New_User_ID|ENTER=Next|TAB=Back|ESC=Cancel'
        elif (logonNo == 7):
            strLine1 = 'Enter_A_New_User_Password|ENTER=Save&Exit|TAB=Back'
        elif (logonNo == 8):
            strLine1 = 'L-ALT=Prev-User|R-ALT=Next-User|ENTER=Next|ESC=Cancel'
        elif (logonNo == 9):
            strLine1 = 'Enter_A_New_User_ID|ENTER=Next|TAB=Back|ESC=Cancel'
        elif (logonNo == 10):
            strLine1 = 'Enter_A_New_User_Password|ENTER=Save&Exit|TAB=Back'
        elif (logonNo == 11):
            strLine1 = 'L-ALT=Prev|R-ALT=Next|DEL=Delete|ENTER=Delete&Exit'
        else:
            strLine1 = 'ALT=Select_Image|L-CTRL=Scr-Mode|R-CTRL=Image-Mode'
            
    elif (inputNo == 1):   
        strLine1 = 'L-ALT=Hide_PIN|R-ALT=Show_PIN|PIN[Numbers_Only_*10]'
    elif (inputNo == 2):   
        strLine1 = 'L-ALT=Hide_Key|R-ALT=Show_Key|ESC=Back|ESC*3=Quit'    
    elif (inputNo == 3):   
        strLine1 = 'Enter_Path_without_file_Name_\'/home/pi/Desktop/Msg\''    
    elif (inputNo == 4):   
        strLine1 = 'Enter_File-Name_only_\'msg\'|L-ALT=Sub_#|R-ALT=Add_#'    
    elif (inputNo == 5):   
        strLine1 = 'DEL=Delete_All|BACK=Back_1|ENTER*2=Next|TAB=Back'    
    elif (inputNo == 6):   
        strLine1 = 'L-ALT=Preset_Footnote_1|R-ALT=Preset_Footnote_2'   
    elif (inputNo == 7):   
        strLine1 = 'L-CTRL=Scn-Mode|R-CTRL=Image-Mode|ESC*2=Quit'
    else:
        strLine1 = 'UpdateF1_:_Sorry_Out_of_Range!'

def  UpdateF2(num):
    
    global strLine1
    
    if (num == 0):
        if (logonNo == 4):
            strLine1 = 'User=' + strUID + '|Image-Mode=' + str(imgMode) + '|Logon=Yes|Pi=4'
        else:
            strLine1 = 'User=' + strUID + '|Image-Mode=' + str(imgMode) + '|Logon=No|Pi=4'
    else:
        strLine1 = 'ERROR_:_UpdateF2-Out_Of_Range!'          
                    
def SaveList():
    
    global genJunk
    global imgMode
    global strPath
    global strLine1
    global strName
    
    oldPath = strPath
    onlName = strName

    genJunk = False
    imgMode = sysImgMode
    content = ''
    strPath = 'Settings/'
    strName = 'publicList'

    UpdatePIN(sysPin, sysKey)#Internal password  SaveList() = LoadList(num) must be the same
    
    try:
        for sub_List in List_Users:
            subContent = '+'.join(sub_List) + '/'
            content += subContent
    except:
        print('ERROR_:_ListToString-Out_Of_Range!')

    Encode1(content)
    WriteFile0(List_Nums)

    strPath = oldPath 
    strName = onlName 
    genJunk = True
    imgMode = 0
    content = ''
    strLine1 = 'Updated_User_List'

def LoadList(num):
    
    global genJunk
    global imgMode
    global strPath
    global strName
    global BZLCOL
    global sysSave
    
    oldPath = strPath
    onlName = strName

    genJunk = False
    imgMode = sysImgMode
    content = ''
    strPath = 'Settings/'
    strName = 'publicList'
    
    List_Users.clear()
    #0=Create encrypted user list | 1=Use Default user list | 2=Load encrypted user list
    try:
        if (num == 0):#Create user list
            BZLCOL = WHITE
            List_Users.append(['Admin', 'admin', 'userID0'])
            List_Users.append(['Max', 'dog', 'userID1'])
            List_Users.append(['Cody', 'cat', 'userID2'])
            List_Users.append(['Group0', 'jumbo', 'GroupID0'])
            SaveList()
            BZLCOL = BLACK
            
        elif (num == 1):#Use preset user list
            BZLCOL = ORANGE
            sysSave = False
            List_Users.append(['Admin', 'admin', 'userID0'])
            List_Users.append(['Max', 'dog', 'userID1'])
            List_Users.append(['Cody', 'cat', 'userID2'])
            List_Users.append(['Group0', 'jumbo', 'GroupID0'])
   
        elif (num == 2):#Load list
            BZLCOL = WHITE
            sysSave = True
            UpdatePIN(sysPin, sysKey)#Internal password  SaveList() = LoadList(num) must be the same
            ReadFile0()
            List_Users.clear()
            content = strLine8.split('/')
    
            for i in range(len(content) - 1):
                subList = content[i]
                subList = subList.split('+')
                List_Users.append(subList)
                
            if (List_Users[0][0] == 'Admin'):
                BZLCOL = BLACK
            else:
                BZLCOL = RED
    except:
        BZLCOL = RED
        strLine1 = 'ERROR_:_LoadList-Out_Of_Range!'

    strPath = oldPath 
    strName = onlName 
    genJunk = True
    imgMode = 0
    content = ''  
    
def ClearSubWin():

    global strUID
    global strGID
    global strPWD
    global strUIDd
    global strGIDd
    global strPWDd
    global strNewUID
    global strNewGID
    global strNewPWD
    global strLine0
    global charM
    
    strPWD = ''
    strUIDd = ''
    strGIDd = ''
    strPWDd = ''
    strNewUID = ''
    strNewGID = ''
    strNewPWD = ''
    strLine0 = ''
    charM = ''
    
    UpdateChar('', '')
    
def UpdateUser(num):

    global strLine0
    global strLine1
    global strUID
    global strGID
    global strPWD
    global strUIDd
    global strGIDd
    global strPWDd
    global logonNo
    global scrMode
    global strNewUID
    global strNewGID
    global strNewPWD
    
    try:
        strNewADM = List_Users[0][0]
    except:
        print('ERROR_:_UpdateUser-List_Is_Empty!')


    if (logonNo == 0):
        strUID = strLine0
        if (strLine0 != ''):
            logonNo = 1
        else:
            strLine1 = 'ERROR:Must_Enter_User-Name/Public-Key!|F1 for Help!'
        strUIDd = strUID
      
    elif (logonNo == 1):
        
        if (strLine0 != ''):
            strGID = strLine0
        else:
            strGID = 'Group0'
        strGIDd = strGID   
        logonNo = 2
        strLine1 = 'Enter=Next(to_Continue!)|ESC=Exit|TAB=Back|F1=Help'
        
    elif (logonNo == 2):
        
        if (strLine0 != ''):
            
            newPWD, newUID = UserSearch(strUID, '', 0)
            
            if (newUID != ''):
                
                if (newPWD == strLine0):

                    strPWD = strLine0
                    if (num == 0):#Normal Logon
                        logonNo = 4
                        scrMode = 2
                    elif (num == 1 and strUID == strNewADM):#Add user logon
                        logonNo = 5
                        strLine1 = 'ADD_USER|Enter=Next|ESC=Exit or F1 for Help!'
                    elif (num == 2 and strUID == strNewADM):#Edit user logon
                        logonNo = 8
                        strLine1 = 'EDIT_USER|Enter=Next|ESC=Exit or F1 for Help!'                        
                    elif (num == 3 and strUID == strNewADM):#Delete user logon
                        logonNo = 11
                        strLine1 = 'DELETE_USER|Enter=Next|ESC=Exit or F1 for Help!'
                    else:
                        logonNo = 4
                        scrMode = 2
                        
                    ClearSubWin()
                else:
                    logonNo = 0
                    strLine1 = 'Password_Incorrect!'
                    strPWD = ''
                    time.sleep(2)
                    ClearSubWin()
                    #print(strLine1)
            else:
                logonNo = 0
                strLine1 = 'No_Such_User!'
                time.sleep(2)
                ClearSubWin()
                #print(strLine1) 
        else:
            ClearSubWin()           
            logonNo = 3
            scrMode = 2

    elif (logonNo == 3):#Quick logon no password
        
        strUID = strUIDd
        strGID = strGIDd
        strPWD = strPWDd
        logonNo == 3
        scrMode = 2
        
    elif (logonNo == 4):#Not used
        logonNo = 5
        
    elif (logonNo == 5):#Edit ADD new User to List 

        if (strLine0 != ''):
            newPWD, newKey = UserSearch(strLine0, '', 0)
            if (newPWD == '' and newKey == ""):
                strNewUID = strLine0
                logonNo = 6
            else:
                strLine1 = 'All_Ready_Used!'
                strUIDd = strLine1
        else:
            strLine1 = 'Must_Have_Name!'
            strUIDd = strLine1

    elif (logonNo == 6):#Edit User List Screen
        
        if (strLine0 != ''):
            newPWD, newKey = UserSearch(strLine0, '', 2)

            if (newPWD == '' and newKey == ""):
                strNewGID = strLine0
                logonNo = 7
            else:
                strLine1 = 'All_Ready_Used!'
                strGIDd = strLine1
        else:
            strLine1 = 'Must_Have_Key!'
            strGIDd = strLine1       
        
        
    elif (logonNo == 7):#Edit User List Screen

        if (strLine0 != ''):
            strNewPWD = strLine0
            sub_List = [strNewUID, strNewPWD, strNewGID]
            List_Users.append(sub_List)
            if (sysSave):
                SaveList()
            ClearSubWin()
            logonNo = 0
        else:
            strPWDd = 'Must_Have_Password!'
            
    elif (logonNo == 8):#Edit User List User Name
        logonNo = 9

    elif (logonNo == 9):#Edit User List User ID
        if (strLine0 != ''):
            strNewGID = strLine0
            UpdateEdit(5)
        logonNo = 10

    elif (logonNo == 10):#Edit User List User Password
        
        if (strLine0 != ''):
            strNewPWD = strLine0
            UpdateEdit(6)
            print('logonNo == 10 - Save and exit')
        if (sysSave):
            SaveList()
        ClearSubWin()
        logonNo = 0
        
    elif (logonNo == 11):#Delete User from List
        
        if (conDel):
            UpdateEdit(3)
            if (sysSave):
                SaveList()
        else:
            strLine1 = 'L-ALT=User-Prev|R-ALT=User-Next|'
            
        ClearSubWin()
        logonNo = 0

    else:
        print('UpdateUser_:_Out_of_Range!')
        ClearSubWin()
        logonNo = 0

    strLine0 = ''
    
    
def UpdateEdit(num):
    
    global strUIDd
    global strGIDd
    global strPWDd
    global indexNo
    global strLine1
    
    totU = len(List_Users) -1 

    if (num == 0):#Look-see mode
        strLine1 = 'L-ALT=Prev-User|R-ALT=Next-User|ENTER=Next'
                    
    elif (num == 1):#Look-see mode up
        strLine1 = 'USER-NUMBER_|_' + str(indexNo + 1) + '_of_' + str(totU + 1)

        if (indexNo < totU):
            indexNo += 1
        else:
            indexNo = 0

    elif (num == 2):#Look-see mode up
        strLine1 = 'USER-NUMBER_|_' + str(indexNo + 1) + '_of_' + str(totU + 1)

        if (indexNo > 0):
            indexNo -= 1
        else:
            indexNo = totU 
            
    elif (num == 3):#DELETE
        if (strUIDd != strUID):
            UserRemove(strUIDd)
            indexNo = 0
        else:
            strLine1 = 'YOU_CANOT_DELETE_YOURSELF'

    elif (num == 5):#Edit update users users Key
        EditUser(strUIDd, strNewGID, 2)
        strLine1 = 'Updated_The_Public_Key_of_' + strUIDd
            
    elif (num == 6):#Edit update users users Password
        EditUser(strUIDd, strNewPWD, 1)
        strLine1 = 'Updated_The_Password_of_' + strUIDd

    try:
        subList = List_Users[indexNo]
        strUIDd = subList[0]
        strGIDd = subList[2]
        strPWDd = subList[1]
    except:
        indexNo = 0
        strUIDd = 'Empty'
        strGIDd = 'Empty'
        strPWDd = 'Empty'        
        
def UserSearch(search, passwd, num):#Check logon password

    global strLine1
    global listNo
    
    passwd = ''
    userid = ''
    listNo = 0
    
    try:
        for sublist in List_Users:
            listNo += 1
            if (sublist[num] == search):
                passwd = sublist[1]
                userid = sublist[2]
                break
    except:
        strLine1 = 'ERROR_:_UserSearch-Out_Of_Range!'
        print(strLine1)

    return (passwd, userid)

def EditUser(search, newStr, num):

    global strLine1
    
    try:
        for sub_List in List_Users:
    
            if (sub_List[0] == search):
                sub_List.pop(num)
                sub_List.insert(num, newStr)
                break
    except:
        strLine1 = 'ERROR_:_EditUser-Out_Of_Range!'
        print(strLine1)   

def UserRemove(search):
    
    global strLine1
    global conDel
    
    try:
        i = 0
        for sub_List in List_Users:
    
            if(sub_List[0] == search):
                List_Users.remove(List_Users[i])
                strLine1 = 'DELETE_USER!_:_' + search
                ClearSubWin()
                break
            i += 1
    except:
        strLine1 = 'ERROR_:_Could_Not_DELETE_USER!' + search
        print(strLine1)
        
    conDel = False
    
def UpdateDspMsg(strLine, strExt):

    global strLine1
    global strLine8
    global strLine9
    global strLine10
    global strLine11
    global dspLine0
    global dspLine1
    global dspLine2
    global dspLine3
    global dspLine4
    global dspLine5
    global dspLine6
    global dspLine7
    global dspLine8
    global dspLine9
    
    dspLine0 = ''
    dspLine1 = ''   
    dspLine2 = ''
    dspLine3 = ''
    dspLine4 = ''   
    dspLine5 = ''
    dspLine6 = ''   
    dspLine7 = ''
    dspLine8 = ''
    dspLine9 = ''
    strLine9 = ''
    strLine11 = ''
    lineCount = 0
    
    if (inputNo != 5):# or inputNo != 6):
        strLine10 = ''
    
    for i in range(0, len(strLine), 1):
        if (i < 50):
            dspLine0 += strLine[i] 
            lineCount = 1
            strLine11 = dspLine0 
            if (inputNo == 5):
                strLine9 = dspLine0 + strExt
        elif (i >= 50 and i < 100):
            dspLine1 += strLine[i]
            lineCount = 2
            if (inputNo == 5):
                strLine9 = dspLine1 + strExt
        elif (i >= 100 and i < 150):
            dspLine2 += strLine[i]
            lineCount = 3
            if (inputNo == 5):
                strLine9 = dspLine2 + strExt
        elif (i >= 150 and i < 200):
            dspLine3 += strLine[i]
            lineCount = 4
            if (inputNo == 5):
                strLine9 = dspLine3 + strExt
        elif (i >= 200 and i < 250):
            dspLine4 += strLine[i]
            lineCount = 5
            if (inputNo == 5):
                strLine9 = dspLine4 + strExt 
        elif (i >= 250 and i < 300):
            dspLine5 += strLine[i]
            lineCount = 6
            if (inputNo == 5):
                strLine9 = dspLine5 + strExt
        elif (i >= 300 and i < 350):
            dspLine6 += strLine[i]
            lineCount = 7
            if (inputNo == 5):
                strLine9 = dspLine6 + strExt
        elif (i >= 350 and i < 400):
            dspLine7 += strLine[i]
            lineCount = 8
            if (inputNo == 5):
                strLine9 = dspLine7 + strExt
        elif (i >= 400 and i < 450):
            dspLine8 += strLine[i]
            lineCount = 9
            if (inputNo == 5):
                strLine9 = dspLine8 + strExt
        elif (i >= 450 and i < 500):
            dspLine9 += strLine[i]
            lineCount = 10
            if (inputNo == 5 and len(dspLine9) < 51):
                strLine9 = dspLine9 + strExt
        else:
            pass
    
    
#==============================================================================
            
def DrawScreen0(scrMode0):#Back screen
    
    if (scrMode0):
        
        screen.fill(ORANGE)
    
        screen.blit(imgImg0, (offsetX , offsetY))
        screen.blit(hudStr7, (rectPosX + 120, rectPosY + 10))
        screen.blit(hudStr8, (rectPosX + 20, rectPosY + 10))
        screen.blit(hudStr9, (rectPosX + 70, rectPosY + 10))
    
        pygame.draw.rect(screen, RED, pygame.Rect(rectPosX - 2, rectPosY - 2, rectSizeX + 4, rectSizeY + 4), 1)
        
        if (debug):
            pass


    else:
        screen.fill(GREEN)
        screen.blit(imgImg1, (0 , 0))
        
        pygame.draw.rect(screen, GREEN, pygame.Rect(9, 13, 588, 20))
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 10, 595, 25), 2) 
        pygame.draw.rect(screen, WHITE, pygame.Rect(15, 195, 360, 70))
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(10, 190, 370, 80), 2)
        
        if (scrMode == 0 and logonNo < 3):
            
            hudStr1 = font1.render('LOGON| %s' %strLine1, True, WHITE)#strLine1 inputNo
            hudStr2 = font1.render('USER_NAME_| %s' %strUIDd, True, RED)#strLine1 inputNo
            hudStr3 = font1.render('GROUP_NAME| %s' %strGIDd, True, GREEN)#strLine1 inputNo
            hudStr4 = font1.render('PASSWORD__| %s' %strPWDd, True, BLACK)#strLine1
            
            screen.blit(hudStr1, (15, 15))
            screen.blit(hudStr2, (20, 200))
            screen.blit(hudStr3, (20, 220))
            screen.blit(hudStr4, (20, 240))
            
            pygame.draw.rect(screen, BLACK, pygame.Rect(15, logonNo * 20 + 200, 360, 18), 1)
            
        else:
            
            hudStr1 = font1.render('EDIT| %s' %strLine1, True, WHITE)#strLine1 inputNo
            hudStr2 = font1.render('USER_NAME_| %s' %strUIDd, True, RED)#strLine1 inputNo
            hudStr3 = font1.render('PUPLIC_KEY| %s' %strGIDd, True, GREEN)#strLine1 inputNo
            hudStr4 = font1.render('PASSWORD__| %s' %strPWDd, True, BLACK)#strLine1
                
            screen.blit(hudStr1, (15, 15))
            screen.blit(hudStr2, (20, 200))
            screen.blit(hudStr3, (20, 220))
            screen.blit(hudStr4, (20, 240))
            
            if (logonNo > 4 and logonNo < 8):
                posY = (logonNo - 5) * 20 + 200
            elif (logonNo > 7 and logonNo < 11):
                posY = (logonNo - 8) * 20 + 200
            else:
                posY = (logonNo - 11) * 20 + 200
            
            if (conDel):
                pygame.draw.rect(screen, RED, pygame.Rect(15, 200, 360, 60), 1)
            else:
                pygame.draw.rect(screen, BLACK, pygame.Rect(15, posY, 360, 18), 1)         
    
def DrawScreen1():#Main screen
    
    screen.fill(ORANGE)
    
    if (logonNo == 4):
        hudStr1 = font1.render('Msg~|%s' %strLine1, True, BLACK)#strLine1
    else:
        hudStr1 = font1.render('Msg~|%s' %strLine1, True, RED)#strLine1 
    hudStr2 = font1.render('PIN#|%s' %strLine2, True, GREEN)
    hudStr3 = font1.render('Key*|%s' %strLine3, True, GREEN)
    hudStr4 = font1.render('Path|%s' %strLine4, True, GREEN)
    hudStr5 = font1.render('Name|%s' %strLine5, True, GREEN)
    hudStr6 = font1.render('Msg#|%s' %strLine9 , True, GREEN)#strLine6 strLine9
    if (len(strLine10) < 50):
         hudStr7 = font1.render('Msg@|%s' %strLine10, True, GREEN)#strLine1 strLine10 strLine12 canI
    else:
        hudStr7 = font1.render('Msg@|ERROR_:_', True, RED)#strLine1 strLine10 strLine12 canI
        
    hudStr8 = font1.render('Msg=|%s' %strLine11, True, GREEN)#strLine11 
    #Result - strLine11 or strLine8 or strLine0 charM charNum strName strPath iCan dummyCount imgMode inputNo setImgMode
    
    screen.blit(imgImg1, (0 , 0))
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 5, 595, 175), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(10, 10, 585, 165))#, 2

    screen.blit(hudStr1, (15, 15))
    screen.blit(hudStr2, (15, 35))
    screen.blit(hudStr3, (15, 55))
    screen.blit(hudStr4, (15, 75))
    screen.blit(hudStr5, (15, 95))
    screen.blit(hudStr6, (15, 115))
    screen.blit(hudStr7, (15, 135))
    screen.blit(hudStr8, (15, 155))

    pygame.draw.rect(screen, BLACK, pygame.Rect(10, inputNo * 20 + 15, 50, 18), 1)


def DrawScreen2():#Long message screen
    
    dspStr0 = font1.render(' : %s' %dspLine0, True, WHITE)#strLine0
    dspStr1 = font1.render(' : %s' %dspLine1, True, WHITE)#strLine0
    dspStr2 = font1.render(' : %s' %dspLine2, True, WHITE)#strLine0
    dspStr3 = font1.render(' : %s' %dspLine3, True, WHITE)#strLine0
    dspStr4 = font1.render(' : %s' %dspLine4, True, WHITE)#strLine0
    dspStr5 = font1.render(' : %s' %dspLine5, True, WHITE)#strLine0
    dspStr6 = font1.render(' : %s' %dspLine6, True, WHITE)#strLine0
    dspStr7 = font1.render(' : %s' %dspLine7, True, WHITE)#strLine0
    dspStr8 = font1.render(' : %s' %dspLine8, True, WHITE)#strLine0
    dspStr9 = font1.render(' : %s' %dspLine9, True, WHITE)#strLine0

    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 185, 595, 220), 2)
    pygame.draw.rect(screen, GREEN, pygame.Rect(10, 190, 585, 210))#, 2
    
    if (inputNo == 5 and rectAddY < 200):
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(40, 195 + rectAddY, 510, 18), 1)
    elif (inputNo == 6):
        pygame.draw.rect(screen, BLACK, pygame.Rect(40, 195, 510, rectAddY), 1)
    
    screen.blit(dspStr0, (15, 195))
    screen.blit(dspStr1, (15, 215))
    screen.blit(dspStr2, (15, 235))
    screen.blit(dspStr3, (15, 255))
    screen.blit(dspStr4, (15, 275))
    screen.blit(dspStr5, (15, 295))
    screen.blit(dspStr6, (15, 315))
    screen.blit(dspStr7, (15, 335))
    screen.blit(dspStr8, (15, 355))
    screen.blit(dspStr9, (15, 375))

def DrawScreen3():
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(50, 210, 250, 170), 2)
    screen.blit(imgDsp0, (55, 215))

def DrawScreen4():
    
    screen.fill((50, 50, 50))
    #screen.blit(imgImg1, (0 , 0))
    hudStr0 = font1.render('SYSTEM|%s' %strLine1, True, WHITE)#strLine1 inputNo
    hudStr1 = font1.render('SYSTEM-KEY|%s' %strPWDd, True, RED)#strLine1
    
    pygame.draw.rect(screen, GREEN, pygame.Rect(9, 13, 588, 20))
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 10, 595, 25), 2) 
    
    pygame.draw.rect(screen, GREEN, pygame.Rect(9, 113, 348, 20))
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 110, 355, 25), 2) 

    screen.blit(hudStr0, (15, 15)) 
    screen.blit(hudStr1, (15, 115))
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(50, 210, 250, 170), 2)
    screen.blit(imgDsp0, (55, 215))


UpdateImgList()
UpdateImage(imgPathList[imgNo])

#================================================================

while not done: # main game loop

    KMInput()
    
    if (scrMode == 0):
        DrawScreen0(False)

    elif (scrMode == 1):
        DrawScreen1()

    elif (scrMode == 2):
        DrawScreen1()
        DrawScreen2()
        if (inputNo == 0 and showImg):
            DrawScreen3()
            
    elif (scrMode == 3):
        DrawScreen4()
        
    else:
        screen.fill(ORANGE)
        done = True
    
    pygame.display.flip()
    FPS.tick(30)
    
#__________________EXIT_THE_GAME____________    

pygame.quit()
sys.exit()




