######################################
# Name: Devon Knudsen
# Date: 27 March 2020
# Assingment: Abraxas
# Written in Python 3
######################################

from sys import stdin

DEBUG = False

# shows stats of the deciphering process, if true
STATS = True

# alphabet used for deciphering (first for ciphers 1 and 2, second for ciphers 3 and 4)
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
# ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"

# denotes the punctuation within the above alphabets, used for normalizing words
PUNCTUATION = " -,;:!?/.'\"()[]$&#%"

# dictionary file as well as potential keys
DICTIONARY_FILE = "dictionary.txt"

# threshold for the acceptable percentage of words
# currently = 53%
THRESHOLD = 0.53

# flag to specify whether or not keys will be processed forwards or backwards.
# the filterKey function moves words larger than 5 chars closer to the front,
# so keeping this as true makes deciphering faster for all example cipher texts
FORWARD = True

# filters out keys that aren't a unique set of characters.
# moves all remaining keys that contain 5 or more chars to the front of the list
# returns the filtered and shifted list
def filterKeys(keys):
    
    # filtering keys
    keysToRemove = []
    for key in keys:
        keyLetters = []
        for i in range(len(key)):
            if(key[i].lower() in keyLetters):
                keysToRemove.append(key)
                
                if DEBUG:
                    print("CURR KEY LIST:" + str(keys))
                
                break
            else:
                keyLetters.append(key[i].lower())
    
    for key in keysToRemove:
        keys.remove(key)
        
        if DEBUG:
            print("REMOVED:" + key)
    
    # shifting keys
    avgKeys = []
    for key in keys:
        if (len(key) >= 5):
            avgKeys.append(key)
    
    for key in avgKeys:
        keys.remove(key)
        keys.insert(0, key)
            
    return keys

# creates a cipher alphabet given a specific key
# then deciphers the given cipher text
# returns deciphered text
def decipher(key, cipherTxt):
    cAlphabet = []
    for char in ALPHABET:
        cAlphabet.append(char)
    
    # creating the cipher alphabet
    for i in range(len(key)):
        cAlphabet.remove(key[i])
        cAlphabet.insert(i, key[i])
    cAlphabet = "".join(cAlphabet)
    
    if DEBUG:
        for k in range(len(ALPHABET)):
            print("INDEX: {}\t ALPHA LETTER:{}\t CALPHA LETTER:{}".format(k, ALPHABET[k], cAlphabet[k]))
    
    # deciphering the cipher text
    decipherTxt = ""
    for j in range(len(cipherTxt)):
        if(cipherTxt[j] in cAlphabet):
            cIndx = cAlphabet.index(cipherTxt[j])
            decipherTxt += ALPHABET[cIndx]
        else:
            decipherTxt += cipherTxt[j]
    
    return decipherTxt

# normalizes candidate text by removing punctuation and new lines
# returns the normalized text
def normalizeTxt(txt):
    for p in PUNCTUATION:
        if(p != "'"):
            txt = txt.replace(p, "")
    
    txt = txt.replace("\n", " ")
    
    return txt

# MAIN
file = open(DICTIONARY_FILE, "r")
pKeys = file.read().rstrip("\n").split("\n")
file.close()

dictionary = []
for word in pKeys:
    dictionary.append(word.lower())

# filter potential keys
pKeys = filterKeys(pKeys)

cipherTxt = stdin.read().rstrip("\n")
cipherTxt = "\n".join(cipherTxt.split("\n"))

# changes the bounds of the follwoing for loop depending
# on if the keys should be processed forwards or backwards
if FORWARD == True:
    start = 0
    end = len(pKeys)
    step = 1
else:
    start = len(pKeys) - 1
    end = -1
    step = -1

# iterating through keys to find the most correct deciphered text
for k in range(start, end, step):
    pTxt = decipher(pKeys[k], cipherTxt)
    words = pTxt.split(" ")
    
    count = 0
    amountOfWords = len(words)
    for x in range(len(words)):
        normalizedWord = normalizeTxt(words[x]).lower()
        
        # if normalization caused two complete words to be held within a single string (removal of a new line)
        if(" " in normalizedWord):
            spaceIndx = normalizedWord.index(" ")
            normalizedWord = normalizedWord.replace(" ", "")
            firstWord = normalizedWord[:spaceIndx]
            secondWord = normalizedWord[spaceIndx:]
            if firstWord in dictionary:
                count += 1
            if secondWord in dictionary:
                count += 1
            
            # increasing count of the amount of words within the candidate text accounts for the two words
            # bound together within a single string by a new line
            amountOfWords += 1
                
        elif(normalizedWord in dictionary):
            count += 1
           
    if((count/amountOfWords) >= THRESHOLD):
        print("KEY: " + pKeys[k])
        print("PLAINTEXT: " + pTxt)
        
        if(STATS):
            print("PERCENTAGE CORRECT: " + str(count/amountOfWords))
            print("COUNT: " + str(count))
            print("LENGTH OF WORDS: " + str(amountOfWords))
            
        exit(0)