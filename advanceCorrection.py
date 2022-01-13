#!/usr/bin/python
import sys
import sys
import subprocess
from subprocess import call
import spacy
import os
import language_tool_python

name = sys.argv[1]
sender = sys.argv[2]
log = sys.argv[3]

import time
time.sleep(.5)
fileObj = open("tempParsed.txt", "r")
msg = fileObj.read()
msg = msg.split('#')
fileObj.close()
time.sleep(.5)
os.remove("tempParsed.txt")
time.sleep(.5)
fileObj = open("tempGramParsed.txt", "r")
gramMsg = fileObj.read()
gramMsg = gramMsg.split('#')
fileObj.close()
time.sleep(.5)
os.remove("tempGramParsed.txt")
time.sleep(.5)


# For ease of debugging
skipLinkedIn = False

# To not look like absolute idiots, some very basic RPI terminology we shouldn't mess up
commonWordsToBeCorrected = ["RCOS", "Rensselaer", "Polytechnic", "administrative",
                            "alumi", "Auxiliary", "athletic", "Blitman", "Bryckwyck",
                            "Colonie", "Darrin", "Farmers", "Folsom", "Graduate", "Marshal",
                            "Heffner", "Houston", "McNeil", "Multicultural", "Panhellenic", "Patroon",
                            "Phalanx", "Pipeline", "Polytech", "Proctor’s", "Theatre", "Puckman", "quotations",
                            "Rathskeller", "Collegiate", "Responsibilities", "ResLife", "Playhouse", "Russell",
                            "Sage", "Dining", "Semesters", "Shelnutt", "Sophomore", "Sorority", "Stacwyck",
                            "Trello", "Troy", "Undergraduate", "Undergraduate", "Administration",
                            "Committee", "Voorhees", "Technologies", "Field", "Armory", "Anderson",
                            "Robison", "Harkness", "Mueller", "Renwyck", "Willie", "Stanton",
                            "Gymnasium", "Academy", "Burdett", "Amos", "Eaton", "Blaw-Knox", "Barton",
                            "Cogswell", "Folsom", "Jonsson", "Jonsson-Rowland", "Lally", "Nason", "Nugent",
                            "Quadrangle", "Ricketts", "Rousseau", "Williams", "Winslow", "Quinnipiac", "RPI"]


# Thank you algo textbook, edit distance (how many edits to get to this string)
def edit_distance(wordInput, wordExpected):
    m = len(wordExpected) + 1
    n = len(wordInput) + 1
    tbl = {}
    for i in range(m): tbl[i, 0] = i
    for j in range(n): tbl[0, j] = j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if wordExpected[i - 1] == wordInput[j - 1] else 1
            tbl[i, j] = min(tbl[i, j - 1] + 1, tbl[i - 1, j] + 1, tbl[i - 1, j - 1] + cost)
    return tbl[i, j]


for x in msg:
    for y in commonWordsToBeCorrected:
        if (x.isupper() and x != y and x != "I" and edit_distance(x, y) <= 2):
            print("Poly-Specific Edit Distance: Consider replacing " + x + " with " + y)
            log += "Poly-Specific Edit Distance: Consider replacing " + x + " with " + y + "\n"



#######################################################################################################


stringToCheck = ""
for x in gramMsg:
    stringToCheck += x + " "

# Now, a VERY basic grammar check
tool = language_tool_python.LanguageTool('en-US')
matches = tool.check(stringToCheck)

# Be wary, the spelling checker is SUPER aggressive against names
# Also, note it is somewhat aggressive against quotations (parser doesn't seem to understand ellipses)
log += "\nNow, the automatic grammar checker's results: \n\n"
for mistake in matches:
    log += str(mistake) + "\n\n\n"
    print(mistake)
    print()


##############################################################################################################


nlp = spacy.load("en_core_web_trf")


# Now, for the automatic fact checking... (Note: code thanks to the following:
# https://stackoverflow.com/questions/51214026/person-name-detection-using-spacy-in-english-lang-looking-for-answer)
def find_persons(text):
    doc2 = nlp(text)
    persons = [ent.text for ent in doc2.ents if ent.label_ == 'PERSON']
    return persons


def numExist(inputString):
    for x in inputString:
        if x.isdigit():
            return True
    return False


actualNames = []
years = []
names = find_persons(stringToCheck)
names = list(set(names))

for x in names:
    if " " in x:
        InsertGradYear = True
        temp = x.split(" ")
        stringName = ""
        for y in temp:
            if numExist(y):
                InsertGradYear = False
                years.append(int(y[1::]))
            else:
                stringName += y + " "
        stringName.rstrip(" ")
        actualNames.append(stringName)
        if (InsertGradYear):
            years.append(-1)

# For Copy Readers to know which information has and hasn't yet been verified (computer could neglect name)
index = 0
for x in actualNames:
    if years[index] == -1:
        print("NOTE: Detected Graduate? Student - " + x)
        log += "NOTE: Detected Graduate? Student - " + x + "\n"
    else:
        print("NOTE: Detected Undergraduate Student - " + x + " Year: " + str(years[index]))
        log += "NOTE: Detected Undergraduate Student - " + x + " Year: " + str(years[index]) + "\n"
    index += 1

# Try to extract information about the individuals
contextForNames = []
# To preventing bounding while still retaining ability to extract information if it exists
stringToCheck = stringToCheck.rjust(90)
stringToCheck = stringToCheck.ljust(90)
for x in actualNames:
    leastIndex = stringToCheck.find(x)
    try:
        endOfSentenceL = stringToCheck[leastIndex - 80:leastIndex].find(".") + leastIndex - 81
        contextString = stringToCheck[endOfSentenceL + 3:leastIndex - 1 + 80]
        contextString = contextString.lstrip(" ")
    except:
        contextString = ""
    contextForNames.append(contextString)

index = 0
for x in contextForNames:
    if x == "":
        print("Error (Automatic Fact Checking of Position Not Possible): Context Information for " + actualNames[index] + "is not available, did you mention their title on first reference?")
        log += "Error (Automatic Fact Checking of Position Not Possible): Context Information for " + actualNames[index] + "is not available, did you mention their title on first reference?" + "\n"
    index += 1


########################################################################################################

from googlesearch import search

# Automatically get linkedin profiles
linkedInProfiles = []
for x in actualNames:
    x += " Rensselaer linkedin"
    foundLinkedIn = False
    for j in search(x, tld="co.in", num=10, stop=10, pause=0):
        if foundLinkedIn is False and "linkedin" in j and "linkedin.com/search/results/" not in j:
            linkedInProfiles.append(j)
            foundLinkedIn = True
    if not foundLinkedIn:
        print("Error (Automatic Fact Checking via LinkedIn Not Possible): " + x)
        log += "Error (Automatic Fact Checking via LinkedIn Not Possible): " + x + "\n"
        linkedInProfiles.append(-1)

from linkedin_scraper import Person, actions
from selenium import webdriver

email = "thebest.polybot@gmail.com"
password = "thePolyBot2000"

# To ease debugging
if skipLinkedIn == False:
    driver = webdriver.Chrome()
    actions.login(driver, email, password)

    linkedInProfilesObj = []
    for x in linkedInProfiles:
        if x == -1:
            linkedInProfilesObj.append(-1)
        else:
            try:
                linkedInProfilesObj.append(Person(x, driver=driver))
                driver = webdriver.Chrome()
                actions.login(driver, email, password)
            except:
                linkedInProfilesObj.append(-1)
                pass

    index = 0
    for x in linkedInProfilesObj:
        if x == -1:
            print("LinkedIn Verification | No LinkedIn Profile(s): " + actualNames[index])
            log += "LinkedIn Verification | No LinkedIn Profile(s): " + actualNames[index] + "\n"
        else:
            if((x.name).replace(" ", "") != actualNames[index].replace(" ", "")):
                print("LinkedIn Verification | Name Issue: " + actualNames[index] + "has closest match to " + x.name)
                log += "LinkedIn Verification | Name Issue: " + actualNames[index] + "has closest match to " + x.name + "\n"
            for l in x.educations:
                combinationOfDescriptionAndDegree = ""
                if(l.description != None):
                    combinationOfDescriptionAndDegree += l.description
                if(l.degree != None):
                    combinationOfDescriptionAndDegree += l.degree
                if(l.institution_name != None):
                    combinationOfDescriptionAndDegree += l.institution_name

                # Okay, potential issue if this thing runs for >70 years, but really?
                if years[index] != -1 and (str(years[index]) in l.to_date or "20" + str(years[index]) in l.to_date):
                    if "RPI" in combinationOfDescriptionAndDegree or "Rensselaer" in combinationOfDescriptionAndDegree:
                        print("LinkedIn Verification | Verified Undergraduate Student " + x.name)
                        log += "LinkedIn Verification | Verified Undergraduate Student " + x.name + "\n"
                else:
                    if years[index] == -1:
                        if ("RPI" in combinationOfDescriptionAndDegree or "Rensselaer" in combinationOfDescriptionAndDegree) and ("PhD" in combinationOfDescriptionAndDegree or "Graduate" in combinationOfDescriptionAndDegree):
                            print("LinkedIn Verification | Verified Graduate Student " + x.name)
                            log += "LinkedIn Verification | Verified Undergraduate Student " + x.name + "\n"
            numMatches = 0
            for j in x.experiences: # Note, this is a heuristic, cannot be FULLY trusted, but verifying positions is 2nd's job
                totalString = ""
                if(j.description != None):
                    totalString += j.description
                if(j.position_title != None):
                    totalString += j.position_title
                if(j.institution_name != None):
                    totalString += j.institution_name
                possibleMatches = contextForNames[index].split(" ")
                # Yes, this is horrible, yes I should strive to make something consecutive biased and multi-word, but
                # titles are dynamic to context and possible positions. So, I though filtering out and using one matches
                # would provide a good heurisitic
                commonFilterWords = ["the", "at", "there", "some", "my", "of", "be", "use", "her", "him", "there", "than",
                                 "and", "this", "an", "would", "first", "a", "have", "each", "make", "to", "from",
                                 "which", "like", "been", "in", "or", "she", "call", "he", "is", "one", "do",
                                 "into", "who", "had", "you", "how", "time", "oil", "that", "by", "their", "has",
                                 "its", "it", "word", "if", "look", "now",  "but", "actually", "said", "reiterated",
                                 "spoke", "interviewed", "was", "not", "two", "find", "more", "long", "up", "on",
                                 "all", "about", "go", "day", "are", "were", "out", "see", "is", "did", "as",
                                 "we", "when", "then", "no", "come", "his", "she", "your", "them", "way", "made",
                                 "they", "can", "these", "could", "may", "I", "said", "so", "people", "part", "however",
                                 "nevertheless", "alternatively", "similarily", "indeed", "think", "believe",
                                 "opinion", "view", "since", "because", "for", "so", "consequential", "therefore",
                                 "this", "while", "at", "last", "another", "because", "an", "from", "during", "the",
                                 "of", "will", "online", "continue", "until", "campus", "take", "undergo", "a", "it",
                                 "its", "through", "throughout", "all", "into", "student", "by", "about", "for",
                                 "will", "have", "one", "can", "should", "will", "within", "among", "the", "recently",
                                 "which", "but", "indefinitely", "been", "their", "what", "that", "despite", "this",
                                 "current", "within", "too", "two", "current", "currently", "with"]
                foundMatchYet = False
                for m in possibleMatches:
                    if foundMatchYet != True and m in totalString and m not in commonFilterWords:
                        print("LinkedIn Verification | Verified Claimed Position for " + x.name)
                        log += "LinkedIn Verification | Verified Claimed Position for " + x.name + "\n"
                        foundMatchYet = True
                else:
                    if m in totalString and m not in commonFilterWords:
                        numMatches += 1
            print("LinkedIn Verification | Claimed Position for " + x.name + " backed by " + str(numMatches + 1) + " word matches")
            log += "LinkedIn Verification | Claimed Position for " + x.name + " backed by " + str(numMatches + 1) \
                   + " word matches" + "\n"
        index += 1

# Call additional file to preform stylistic suggestion to author
with open("tempGramParsed.txt", 'w') as f:
    f.write('#'.join(gramMsg))
f.close()

with open("tempLogParsed.txt", 'w', encoding="utf-8") as f:
    f.write(str(log))
f.close()


call(["python", "stylisticSuggestions.py", name, sender])
