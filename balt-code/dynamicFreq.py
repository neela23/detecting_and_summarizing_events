#import feedparser  
import re
import networkx as nx
from random import choice
#from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import heapq
import datetime
import json
import dateutil.parser
import time
from scipy import stats
from collections import deque
import csv
#********************************************************************** Data cleaning ******************************************************#

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

def preprocessKeywords(text):
        text = removeHashTag(text)
	text = stemText(text)
	text = removeStopwords(text)
        return text

def getWords(text):
	text = re.sub("<.*?>","",text.lower())
	text = re.sub(r"http\S+", "", text)                                              # Removing html tags if present
	words = re.compile(r'[^A-Z^a-z]+').split(text)                              #Getting words
	return words


#***********************************************************************************************************************************************

def storeKeywords(keywords):
	keywordFile = open('keyword.txt','w+')
	for word in keywords:
#		keywordFile.write(str(dict(word)))
		keywordFile.write(word)
		keywordFile.write('\n')
		#print(word)


def returnKeywordFromFrozenSet(node):
	keywordDict = dict(node)
	return keywordDict["keyword"] 

def retrieveKeywords():
	keywordFile = open('keyword.txt','r')

def storeDetails(keywords, i):
#	global keywordDict
        global frequencyDict
	for word in keywords:
		#keywordDict[word] = i
		frequencyDict[word] = keywordDict.setdefault(word, 0)+1

def decreaseEdgeWeights():
	global edges, edgeIndex, G, centralityQueue
	edgeIndex = (0 if edgeIndex+1>=6 else edgeIndex+1)
	if(len(edges)== 6):
		for edge in edges[edgeIndex]:
			split = edge.split(',')
			u = split[0]
			v = split[1]
			G[u][v]['weight']-=1
			if G[u][v]['weight'] == 0:
				G.remove_edge(u,v)
			if G.degree(u)==0:
                                G.remove_node(u)
				centralityQueue.pop(u, None)
                        if G.degree(v)==0:
                                G.remove_node(v)
				centralityQueue.pop(v, None)
				
		#deg = G.degree()
		#to_remove = [n for n in deg if deg[n] <=0]
		#G.remove_nodes_from(to_remove)
#********************************************** Twitter********************

def getTextFromJson(fileName, i):
	global keywordDict
	freq = dict()
	tweetsList = open(fileName, 'r')# open('tweets.txt','r')
	#test = tweetsList.read()
	tweets = []
	
	with open(fileName, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                for line in reader:
                        tweetData = line[1]
                        tweet = getWords(tweetData)
                        tweetKeywords = preprocessKeywords(tweet)
			for word in tweetKeywords:
				 freq[word] = freq.get(word, 0.0) + 1
                        #tweetDate = "10-06" # Not used remove sometime
                        #if len(tweetKeywords) > 1:
                                #createGraph(tweetKeywords, tweetDate)
	return freq;
	'''
	for line in tweetsList:
		
		tweetText = line.partition(' ')
		tweetData = tweetText[2]
		tweetDate = '01-02'# Using dummy. Can add if needed
		
		tweet = getWords(tweetData)
		tweetKeywords = preprocessKeywords(tweet)
		#storeDetails(tweetKeywords,i)	
                #addKeywordsToDict(tweetKeywords, formattedDate)
		if len(tweetKeywords) > 1:
	                createGraph(tweetKeywords, tweetDate)
	'''

#******************************************************Graph*******************************************

def createGraph(text, date):
	global G, edges, edgeIndex
	listOfEdges = []
	for i in range(len(text)):
		G.add_node(text[i])
		for j in range(0, i):
			edge = text[i] + ',' + text[j]
			listOfEdges.append(edge)
			if(G.has_edge(text[j],text[i])):
				G[text[j]][text[i]]['weight'] += 1
			else:
				G.add_edge(text[i], text[j], weight=1)
	if len(edges)==6:
		edges[edgeIndex] = listOfEdges
	else:
		edges.append(listOfEdges)
	


# ------------------------------------------------------------------Centrality--------------------------------------

def calculateEigenvector(graph):
		centrality = nx.eigenvector_centrality(graph, weight = 'weight')
		return centrality

def calculateBetweenness(graph):
	approx = len(G) if len(G)<20 else 20
	centrality = nx.betweenness_centrality(graph, k = approx, normalized=True, weight = 'weight', endpoints=False, seed=None)
	return centrality

def calculateHits():
	h,a = nx.hits(G, max_iter= 30,  nstart=None, normalized=True)
	return h,a

def calculatePageRank():
	pr = nx.pagerank(G, weight = 'weight')
	return pr


#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def addKeywordsToDict(keywords, formattedDate):
	global keywordDict
        #formattedDate = (date.tm_year*10000) + (date.tm_mon*100) + date.tm_mday
        #print(formattedDate)   
        for word in keywords:
                keywordDict[word]=formattedDate
        # Clear old keywords
        oldKeywords = [key for key,value in keywordDict.items() if value < formattedDate-100]

        for key in oldKeywords:
                del keywordDict[key]
                G.remove_node(key)      
        #for key in oldKeywords:   
	
RSS_URLS = ['http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305','http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7','http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5','http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa','http://feeds.reuters.com/Reuters/domesticNews','http://feeds.reuters.com/Reuters/worldNews','http://feeds.reuters.com/Reuters/PoliticsNews'] #'http://feeds.reuters.com/reuters/topNews'

keywords = ["baltimore", "riots"]#, "Obama", "Elections","U.S."]
feeds = []

#keywordDict = dict()

#graphDict = dict()

G= nx.Graph()

#G = nx.read_weighted_edgelist('/scratch2/navudai/baltimore/graph/graph181weighted.edgelist')
#print len(G)
#G = nx.convert_node_labels_to_integers(G)


'''
count = 0 

for url in RSS_URLS:
	test = feedparser.parse(url).entries
	feeds.extend(feedparser.parse(url).entries); # Use feeds.append if you want a 2D structure, each row 	
	
for post in feeds:
	summary = getWords(post.title+ " "+post.summary)	
	if any(x in summary for x in keywords):	
		formattedDate = (post.published_parsed.tm_year*10000) + (post.published_parsed.tm_mon*100) + post.published_parsed.tm_mday
		count=count+1
		keyword = preprocessKeywords(summary)
		addKeywordsToDict(keyword, formattedDate)
		createGraph(keyword, post.published)	
'''

tweetFiles = []

frequencyDict = dict()
edges = []
edgeIndex = -1
keywordDict = dict()
centralityQueue = dict()

getStopwords()

for i in range(1,385):
	fileName = "/scratch2/navudai/baltimorefiles/file"+`i`+".csv"
	tweetFiles.append(fileName)


for i in range(0, 384):#range(len(tweetFiles)):
	decreaseEdgeWeights()
	frequencyDict = getTextFromJson(tweetFiles[i], i+1)
	
	#print('Keywords', len(G))


	#`````````````````````````````````````````````````````````Remove this~```````````````````````````````````````````````````````````````
	#if i+1 < 208:
	#	continue
	
	#```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````


	#frequencyDict = calculateEigenvector(G)	
	
	maxKey = max(frequencyDict , key = frequencyDict.get)
	maxC = frequencyDict[maxKey]
	#print maxKey, maxC
	for key in frequencyDict:
		frequencyDict[key] = frequencyDict[key]/maxC
	
	
	
	for node in frequencyDict:
		cQueue = centralityQueue.setdefault(node, deque())	
		
		if len(cQueue)>=5:
			cQueue.popleft()
		cQueue.append(frequencyDict[node])
		centralityQueue[node] = cQueue
	
	#for node in centralityQueue:
	
		y = centralityQueue[node]
		x = []
		for k in range(len(y)):
			x.append(k+1)
		slope =0
		if len(y)>1:
			slope, intercept, r_value, pvalue, std_err = stats.linregress(x,y)
		#print (node, frequencyDict[node],x,y,slope)
		frequencyDict[node]*=slope
	
	'''
	
	numberOfElements = len(G) if len(G)<100 else 100;
	
	etarget = heapq.nlargest(numberOfElements, frequencyDict, key = frequencyDict.get)                       # Pick elements with largest centrality.
	#ptarget = htarget = heapq.nlargest(numberOfElements, pr, key = pr.get)
 	
	'''
	
	fileName = "/scratch2/navudai/baltimore/dynamicFreq/freq"+`i+1`+".txt"

	ecentral = open(fileName,'w')
	
	for node in frequencyDict:
		ecentral.write(node)
		ecentral.write(" ")
		ecentral.write(str(frequencyDict[node]))
		#ecentral.write(" ")
                #ecentral.write(str(frequencyDict[node]))
        	ecentral.write('\n')
	
	'''
	#if(i%50 is 0):
		#gloc = "/scratch2/navudai/baltimore/graph/graph"+`i+1`+".weighted.edgelist";
	#	nx.write_weighted_edgelist(G, gloc)
	
	bfileName = "/scratch2/navudai/bcentrality/bcentrality"+`i+1`+".txt"

        bcentral = open(bfileName,'w')
	
        for node in btarget:
                bcentral.write(node)
                bcentral.write(" ")
                bcentral.write(str(bcentrality[node]))
		bcentral.write(" ")
                bcentral.write(str(frequencyDict[node]))
                bcentral.write('\n')

	hfileName = "/scratch2/navudai/hubs/hub"+`i+1`+".txt"

        hcentral = open(hfileName,'w')

        for node in htarget:
                hcentral.write(node)
                hcentral.write(" ")
                hcentral.write(str(h[node]))
		hcentral.write(" ")
                hcentral.write(str(frequencyDict[node]))
                hcentral.write('\n')

	afileName = "/scratch2/navudai/authorities/authority"+`i+1`+".txt"

        acentral = open(afileName,'w')

        for node in atarget:
                acentral.write(node)
                acentral.write(" ")
                acentral.write(str(a[node]))
		acentral.write(" ")
                acentral.write(str(frequencyDict[node]))
                acentral.write('\n')

'''

	#time.sleep(60) # 1=1second
	#nx.write_weighted_edgelist(G, 'graph.weighted.edgelist')

