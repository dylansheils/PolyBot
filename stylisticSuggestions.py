#!/usr/bin/python
import sys
import os
import subprocess
import time
from os import listdir
from os.path import isfile, join

global log
name = sys.argv[1]
sender = sys.argv[2]
log = sys.argv[3]

time.sleep(.5)
fileObj = open("tempGramParsed.txt", "r")
gramMsg = fileObj.read()
gramMsg = gramMsg.split('#')
fileObj.close()
os.remove("tempGramParsed.txt")
time.sleep(.5)
import subprocess
import sys

# Just for future convience
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("nltk")

import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk import tokenize

# Markov Language Repetition Detector
##############################################################################################################
import markovify
timestr = time.strftime("%Y%m%d_%H%M%S")

# Supposed Folder Location, Create one if it does not already exist
folderName = (str(name).strip()).replace(" ", "")
articleName = folderName + "_art_" + str(timestr).strip() + ".txt"
if folderName not in [pos for pos in os.listdir("./historicArticles/")
                               if os.path.isdir(os.path.join("./historicArticles/", pos))]:
    try:
        os.mkdir("./historicArticles/" + folderName)
    except:
        pass
    
# Get all prior article names
totalPath = "./historicArticles/" + folderName + "/"
articles = [f for f in listdir(totalPath) if isfile(join(totalPath, f))]
articlesContent = ""
worth = 1
number = 0
models = []
worths = []

input_source = []
line = ""
for words in gramMsg:
    if ("." in words or "!" in words or "?" in words) and words.count('"') <= 0 and words.count('”') <= 0 \
            and words.count('“') <= 0 and words.count(".") == 1:
        line += " " + words[:words.index(".")] + "."
        input_source.append(line[1:].replace('"', '').replace('”','').replace('“','').lstrip())
        line = words[words.index("."):]
    else:
        line += " " + words

storMessage = ""
for i in input_source:
    storMessage += i + " "

import pysimilar
from pysimilar import compare
with open(totalPath + articleName + "temp", 'w') as f:
    f.write(storMessage)
f.close()
pysimilar.extensions = '.txt'

log += "\n\n\n"
fileOutputs = []
for article in articles:
    if ".txt" in article:
        fileObj = open(totalPath + article, "r")
        articlesContent = fileObj.read()
        fileOutputs.append(articlesContent)
        # Read in all articles, put in up to 50% more weight on newer
        models.append(markovify.Text(articlesContent, state_size=2))
        worths.append(1 + (number/(2*len(articles))))
        number += 1
        fileObj.close()
        comparison_result = compare(totalPath + articleName + "temp", totalPath + article)
        if(comparison_result > .38):
            print("PolyBot | Similarity Detection | Beginning Portion of Similar Article by you: ", articlesContent[:128])
            log += "PolyBot | Similarity Detection | Beginning Portion of Similar Article by you: " + articlesContent[:128]
os.remove(totalPath + articleName + "temp")
text_model = -1
if len(models) > 0:
    text_model = markovify.combine(models, worths)

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

from thefuzz import fuzz

top5Lines = [" ", " ", " ", " ", " "]
top5Generated = [" ", " ", " ", " ", " "]
top5LinesValue = [0, 0, 0, 0, 0]

lineNum = 1
for line in input_source:
    if text_model != -1:
        generatedLine = ""
        priorVal = 0
        splicedInputString = line.split()
        for i in range(len(splicedInputString)-2):
            if text_model != -1 and len(splicedInputString) >= 2:
                inputString = splicedInputString[i] + " " + splicedInputString[i+1]
                generated = " "
                try:
                    generated = str(text_model.make_sentence_with_start(inputString, False))
                except:
                    try:
                        generated = str(text_model.make_sentence())
                    except:
                        pass
                    pass
                totalDistance = ((fuzz.ratio(generated, line) + 10)/100)/2
                replacedVal = False
                for i in range(len(top5LinesValue)):
                    if(totalDistance > top5LinesValue[i] and totalDistance > .20 and not replacedVal):
                        top5LinesValue[i] = totalDistance
                        top5Generated[i] = generated
                        top5Lines[i] = line
                        replacedVal = True
        lineNum += 1

for i in range(len(top5Lines)):
    if(top5Lines[i] != " "):
        print("PolyBot | Diversify Writing Suggestion | Computer Guessed: ", top5Generated[i], " You Wrote: ", top5Lines[i])
        log += "PolyBot | Diversify Writing Suggestion | Computer Guessed: " + top5Generated[i] + " You Wrote: " + top5Lines[i] + "\n\n"
log += "\n\n\n\n"
####################################### Sentiment Analysis #################################################
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def checkMeaning(value, pos, line, samples):
    if value > .28 and samples == 1:
        if pos == True:
            print("PolyBot | Reconsider Excessive Positivity for line: ", line)
            log += "PolyBot | Reconsider Excessive Positivity for line: " + line + "\n"
        else:
            print("PolyBot | Reconsider Excessive Negativity for line: ", line)
            log += "PolyBot | Reconsider Excessive Negativity for line: " + line
def getSentiments(sourceData, samplesInCollection):
    if(samplesInCollection == 0):
        return 0, 0, 0, 0
    averageSentiment = 0.00
    averageNegSentiment = 0.00
    averagePosSentiment = 0.00
    averageNeuSentiment = 0.00
    sid = SentimentIntensityAnalyzer()
    for line in sourceData:
        ss = sid.polarity_scores(line)
        for k in sorted(ss):
            if k == 'compound':
                averageSentiment += ss[k] / len(input_source)
            if k == 'neg':
                averagePosSentiment += ss[k] / len(input_source)
                checkMeaning(ss[k], False, line, samplesInCollection)
            if k == 'neu':
                averageNeuSentiment += ss[k] / len(input_source)
            if k == 'pos':
                averagePosSentiment += ss[k] / len(input_source)
                checkMeaning(ss[k], True, line, samplesInCollection)
    return averageSentiment/samplesInCollection, averageNegSentiment/samplesInCollection, \
           averagePosSentiment/samplesInCollection, averageNeuSentiment/samplesInCollection

sentences = []
for sources in fileOutputs:
    lines_list = tokenize.sent_tokenize(sources)
    sentences.extend(lines_list)

avg, neg, pos, neu = getSentiments(sentences, len(fileOutputs))
avgArt, negArt, posArt, neuArt = getSentiments(input_source, 1)

log += "\n\n\n"
print("PolyBot | Sentiment Analysis, Article (comparison with general English writing): Positivity %: ", str(posArt * 100),
      " Negativity %: ", str(negArt * 100), " Neutrality %: ", str(neuArt * 100), " Overall Sentiment (-1 [negative] - 1 [positive]): ", str(avgArt * 100))
log += "PolyBot | Sentiment Analysis, Article (comparison with general English writing): Positivity %: " + str(posArt * 100) + \
      " Negativity %: " + str(negArt * 100) + " Neutrality %: " + str(neuArt * 100) + " Overall Sentiment (-1 [negative] - 1 [positive]): " + str(avgArt * 100)
print("PolyBot | Sentiment Analysis, Article (comparison with your historic Poly writing): Positivity Deviation %: " +
      str((pos - posArt) * 100) + " Negativity Deviation %: " +
      str((neg - negArt) * 100) + " Neutral Deviation %: " +
      str((neu - neuArt) * 100) + " In total Deviation %: " + str(avg - avgArt) * 100)
log += "PolyBot | Sentiment Analysis, Article (comparison with your historic Poly writing): Positivity Difference %: " + \
      str((pos - posArt) * 100) + " Negativity Difference %: " + \
      str((neg - negArt) * 100) + " Neutral Difference %: " + \
      str((neu - neuArt) * 100) + " In total Difference %: " + str((avg - avgArt)*100)

with open(totalPath + articleName, 'w') as f:
    f.write(storMessage)
f.close()

#################### PROGRAM EXIT #########################
# Send the resulting email to the sender
from subprocess import call
call(["python", "sendLogViaEmail.py", name, sender, log])