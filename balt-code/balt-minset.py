import sys
import nltk
from nltk.stem import WordNetLemmatizer
import re
import heapq
import csv

# U is keywords-centality dictionary
'''
1. U
2. Have dictionary with tweetid as key, value is a dictionary with 1. tweet 2. weight 3. keywords
3. Set I is tweet ids of selected tweets, we maintain K, a set of keywords that are selected already
From for all tweets t find weight[t]/ |keywords - K|, and minimize it. Ignore the tweet if denominator is 0
'''


# ~ ~ ````````````````````````````````` 

stopwordlist = []
def getStopwords():
        global stopwordlist
        stopwordfile = open('/scratch2/navudai/stopwordlist.txt' , 'r')
        #stopwords = []
        for line in stopwordfile:
                for word in line.split():
                        stopwordlist.append(word)
        #stopwords = stopwordlist.split()
        print stopwordlist
        #return stopwords

def removeStopwords(text):
        #stopwordlist = ge
        stopped = [x for x in text if x.lower() in stopwordlist]
        text = [x for x in text if x.lower() not in stopwordlist]
        text = [x for x in text if len(x) > 1]
        return text

def removeHashTag(text):
        cleanedText = []
        for word in text:
                word= word.replace("#","")
                cleanedText.append(word)
        return cleanedText

def stemText(text):
        wordnet_lemmatizer = WordNetLemmatizer()
        stemmed = []
        for word in text:
                stemmed.append(wordnet_lemmatizer.lemmatize(word))
        return stemmed

def getWords(text):
        text = re.sub("<.*?>","",text.lower())
        text = re.sub(r"http\S+", "", text)                                              # Removing html tags if present
        words = re.compile(r'[^A-Z^a-z]+').split(text)                              #Getting words
        return words

def preprocessKeywords(tweet):
	text = getWords(tweet)
        text = removeHashTag(text)
        text = stemText(text)
        text = removeStopwords(text)
        return text

def populateTweetDict(keywordList):
        #keywordList = heapq.nlargest(numberOfElements, U, key = U.get)
        k=0
        tweetDict = dict()
        with open(tweetFiles[i], 'rb') as csvfile:
		reader = csv.reader(csvfile) 
        	for line in reader:
			tweet = line[1]
			tweetId = line[2]
						
                	tweetDetails = dict()
	                text = preprocessKeywords(tweet)
        	        keywordsPresent = [word for word in text if word in keywordList]
                	#print keywordsPresent
	                weight = 0.0
        	        for word in keywordsPresent:
                	        weight+=float(U[word])
	                tweetDetails['tweet'] = tweet
        	        tweetDetails['weight'] = weight
                	tweetDetails['keywords'] = list(set(keywordsPresent))
	                tweetDict[tweetId] = tweetDetails
			
	return tweetDict

tweetFiles = []
keywordFiles = []
story = dict()
storyFile = open('', 'w')

for i in range(1,385):
        fileName1 = "/scratch2/navudai/baltimorefiles/file"+`i`+".csv"
        tweetFiles.append(fileName)
        fileName2 = "/scratch2/navudai/baltimore/dynamicECall/ecentrality"+`i`+".txt"
        keywordFiles.append(fileName2)

for i in range(0, 385):
	storyFile.write(str(i+1))
	storyFile.write('\n')	
	print i
	#storyFile = open( "/scratch2/navudai/boston/code/top100files/topTweet"+`i`+".txt", 'w')
	# Get U
	#storyFile.write(str(i+1))
	U = dict()
	keywordRead = open(keywordFiles[i], 'r')
	k=0
	#keywordList = []
	for line in keywordRead:
		line = line.strip()
		keyword, temp, weight  = line.partition(' ')
		#print i, keyword, weight
		#keywordList.append(keyword)
		U[keyword] = float(weight)
		#if k is 10: # Choosing top10 keywords for every hour
		#	break

	numberOfElements = 20
        keywordList = heapq.nlargest(numberOfElements, U, key = U.get)
	tweetDict = populateTweetDict(keywordList)
		
		#print tweet
	#print keywordList
	I = []
	selectedKeywords = []
	
	# find weight[t]/ |keywords - K|, and minimize it. Ignore the tweet if denominator is 0
	# Greedy Algorithm for minimum set cover!
	#storyFile.write(str(i))
	#storyFile.write('\n')

	requiredKeywordCount = numberOfElements
	while len(selectedKeywords) < requiredKeywordCount:
			minVal =  sys.maxint
			minId = -1
			
			for tweetId, tweetDetails in tweetDict.items():
				denominatorSet = [word for word in tweetDetails['keywords'] if word not in selectedKeywords] # Newly added keywords
				#print denominatorSet
				if len(denominatorSet) is 0:
					continue
				val = tweetDetails['weight'] / len(denominatorSet)
				if val < minVal:
					minVal = val
					minId = tweetId
			if minId is -1: # Will never happe	
				#oldKeywords = heapq.nlargest(numberOfElements, U, key = U.get)
				numberOfElements = numberOfElements + requiredKeywordCount - selectedKeywords
				keywordList = heapq.nlargest(numberOfElements, U, key = U.get)
				#keywordList = [word for word in newKeywords if word not in oldKeywords]
				tweetDict = populateTweetDict(keywordList)
				continue
	
			I.append(minId)
			#tweetD = dict()
			tweetDetails = tweetDict.get(minId)

			tweetText = tweetDetails.get('tweet')
			
			storyFile.write(str(minId))
			storyFile.write(" ")
			storyFile.write(tweetText)
			storyFile.write('\n')
			
			newKeywords = tweetDetails.get("keywords")
			selectedKeywords.extend(newKeywords)
			selectedKeywords = list(set(selectedKeywords))
			#print len(selectedKeywords)
			#print I
			#print 'selected: ', selectedKeywords	
			#story[str(i)] = I
	#storyFile.close()
	
'''
storyFile = open('story.txt', 'w')
for i, I in story.items():
	for tweetId in I:
		tweetDetails = (tweetDict.get(tweetId))
		storyFile.write
'''
	#print tweetDict
	
	#tweetDet = tweetDict[minId]
	
	#selectedKeywords.extend(tweetDetails['keywords'])
	#print tweetDetails['tweet']
	
