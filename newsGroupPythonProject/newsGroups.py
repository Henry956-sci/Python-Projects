import os
import re

#opens the stop words file so it can  be read, checks to make sure it is opened using try and except
rfhand = open("C:\\Computer Science\\Class Stuff\\Python\\Projects\\Project 1\\newsgroups\\stopWords.txt")
try:
    rfhand = open("C:\\Computer Science\\Class Stuff\\Python\\Projects\\Project 1\\newsgroups\\stopWords.txt")
except:
    print("Unable to open stop words file")
    exit()
#reads the words from the file and puts them into a list
stopWords = rfhand.read().split()

#create 3 dictionaries, one for each of the categories
OrgPerc = dict()
HourPerc = dict()
WordOccurPerc = dict()

#this is the path of the folder newsgroups, which is where all the files are located
path = "C:\\Computer Science\\Class Stuff\\Python\\Projects\\Project 1\\newsgroups"
#changes the OS directory position to this path
os.chdir(path)

#Function used for obtaining the organization from the message
def read_fileOrg(file_path):
    with open(file_path, 'r') as f:
        #checks every line
        for line in f:
            #strips every line of white space on the right
            line = line.rstrip()
            #checks if the line starts with 'Organization: '
            if line.startswith('Organization: '):
                #trims away the 'Organization: ' from the line, leaving us with the organization
                org = line[14:]
                #returns organization as the string org
                return org

#Function used for obtaining the hour from the message
def read_fileHour(file_path):
    with open(file_path, 'r') as f:
        #checks every line
        for line in f:
            #strips every line of white space on the right
            line = line.rstrip()
            #checks if the line starts with 'Date: '
            if line.startswith('Date: '):
                #finds the location of the timezone, which is located after the time
                timezone = line.find('GMT')
                #finds the time, which is 9 spaces to the left from the timezone and trims everything else away
                time = line[(timezone-9):timezone]
                #finds the hour by trimming the other numbers from time away
                hour = time[:2]
                #returns hour
                return hour

#Function used for finding the words occuring the subject and body of the messages
def read_fileWord(file_path, wordCount):
    with open(file_path, 'r') as f:
        #declaration of variables, and a blacklist which is a list of characters which are not allowed in the words
        subWords = ''
        mainWords = ''
        foundLine = False
        blackList = ['[', ']', '....','...','..', '=', ',', '@', '_', '-', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?','/','\\','|', '}' '{', '~', ':', '"',r'\d']
        #checks every line
        for line in f:
            #trims away all white space from the right of the line
            line = line.rstrip()

            #if the identifying line that shows that the body has started is found, then it beginds to read every line in the message
            if foundLine == True:
                #checks evey word in the line
                for word in line.split():
                    #checks to see that the word is not a stop word
                    if word not in stopWords:
                        #checks the blacklist, if the word contains a blacklisted character, it deletes it
                        for i in blackList:
                            word = word.replace(i,'')
                        #creates a list of words found in the body
                        mainWords = mainWords +' '+ word
                        #increments word count by one everytime a word is added
                        wordCount += 1

            #checks if the line starts with 'Subject: '
            if line.startswith('Subject: '):
                #then it checks if the line has Re:
                if line.find('Re: ') != -1:
                    #in which case, it prepares to trim off the length of subject and re
                    subTrim = len('Subject: Re: ')
                #otherwise
                else:
                    #it just trims the length of subject
                    subTrim = len('Subject: ')
                
                #new line is acquired after trimming
                newLine = line[subTrim:]
                #checks every word from the new line
                for word in newLine.split():
                    #checks to see that the word is not a stop word
                    if word not in stopWords:
                        #checks the blacklist, if the word contains a blacklisted character, it deletes it
                        for i in blackList:
                            word = word.replace(i,'')
                        #creates a list of words found in the subject
                        subWords = subWords +' '+ word
                        #increments word count by one everytime a word is added
                        wordCount += 1
            
            #this is the identifying line showing that the body has started in the message
            if line.startswith('In article'):
                foundLine = True

        #creates a list from the words from in the body and subject
        totWords = subWords + ' ' + mainWords
        #returns totWords as well as wordCount
        return totWords, wordCount

count = 0
wordCount = 0
#PROCESSING ORGANIZATION OCCURANCE
for index, file in enumerate(os.listdir()):
    #if the file is the stop words, it won't check it
    if file == "stopWords.txt":
        continue
    #checks every other file, as stated in the instructions
    if index % 2 != 0:
        continue
    
    #assigns the path of the file to a variable
    file_path = f"{path}\{file}"

    #this variable is sent to the function so that it can read the file
    org = read_fileOrg(file_path)

    #if nothing is found, skip it
    if org == None:
        continue
    count += 1
    #if the organization isn't already in the dictionary, add it with the value of one
    if org not in OrgPerc:
        OrgPerc[org] = 1
    else:
    #otherwise, increase it by 1
        OrgPerc[org] = OrgPerc[org] + 1

#checks every key in the dictionary
for key in OrgPerc:
    #gets the percentage by getting the count of the times the word accurs which is stored in the value of the dictionary, divides it by the count of the messages. giving the percentage of messages each org sent
    OrgPerc[key] = round(((OrgPerc[key]/count) * 100), 2)

#resets count
count = 0
#PROCESSING HOUR PERCENTAGE
for index, file in enumerate(os.listdir()):
    if file == "stopWords.txt":
        continue
    if index % 2 != 0:
        continue

    file_path = f"{path}\{file}"

    #gets hour from reading the file
    hour = read_fileHour(file_path)
    #if nothing is found, skip
    if hour == None:
        continue
    count += 1
    #if the hour isn't already in the dictionary, add it with the value of one
    if hour not in HourPerc:
        HourPerc[hour] = 1
    else:
    #otherwise, increase it by 1
        HourPerc[hour] = HourPerc[hour] + 1

for key in HourPerc:
    #gets the percentage by getting the count of the times the word accurs which is stored in the value of the dictionary, divides it by the count of the messages. giving the percentage of messages sent in each hour
    HourPerc[key] = round(((HourPerc[key]/count) * 100), 2)

#PROCESSING WORD PERCENTAGE
for index, file in enumerate(os.listdir()):
    if file == "stopWords.txt":
        continue
    if index % 2 != 0:
        continue

    file_path = f"{path}\{file}"

    #gets total words and word count from the function
    totWords, wordCount = read_fileWord(file_path,wordCount)
    #if nothing is found, skip
    if totWords == None:
        continue
    #if nothing is found, skip
    if wordCount == None:
        continue
    #checks all the words in the total words list
    for word in totWords.split():
        #if empty, skip
        if word == ' ':
            continue
        #if the word isn't already in the dictionary's values, add it with the value of one
        if word not in WordOccurPerc:
            WordOccurPerc[word] = 1
        else:
        #otherwise, increment the value by 1
            WordOccurPerc[word] = WordOccurPerc[word] + 1

#gets the percentage of occurrences of each word by getting the count of each word, which is stored in the value, and dividing it by the total word count then multiplying that by 100
for word in WordOccurPerc:
    WordOccurPerc[word] = round(((WordOccurPerc[word]/wordCount) * 100), 2)

#sorts the dictionaries in descending order according to their values
sortedOrgVal = sorted(OrgPerc.values(), reverse=True)
sortedOrg = {}
for i in sortedOrgVal:
    for k in OrgPerc.keys():
        if OrgPerc[k] == i:
            sortedOrg[k] = OrgPerc[k]
            

sortedHourVal = sorted(HourPerc.values(), reverse=True)
sortedHour = {}
for i in sortedHourVal:
    for k in HourPerc.keys():
        if HourPerc[k] == i:
            sortedHour[k] = HourPerc[k]
            

sortedWordVal = sorted(WordOccurPerc.values(), reverse=True)
sortedWord = {}
for i in sortedWordVal:
    for k in WordOccurPerc.keys():
        if WordOccurPerc[k] == i:
            sortedWord[k] = WordOccurPerc[k]
            
#creates a list of tuples using the sorted dictionaries
O = list(sortedOrg.items())
H = list(sortedHour.items())
W = list(sortedWord.items())

#print everything
print('Ogranizations:')
print(O,'\n')
print('Hours:')
print(H,'\n')
print('Words:')
print(W,'\n')