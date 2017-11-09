import datetime
import json
import dateutil.parser
import time
import csv

#2013-04-22 17:50:49-04:00

#f=open("/scratch2/navudai/boston/boston-sorted.txt")
i=0
phr=''
pday=''


with open("/scratch2/navudai/baltimore/balt-sorted.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:

        #tweet_long = line[2]
        tId = line[2]; #tweet_long.partition(',')[2]

        tweetText = line[1]

        #2015-04-17 21:39:15-04:00

        tDate = line[0]

        tweetDate = datetime.datetime.strptime(tDate, "%Y-%m-%d %H:%M:%S-04:00")
        day=tweetDate.day
        hr=tweetDate.hour
        if i is 0 or hr is not phr:
                phr=hr
                #pday=day
                print i+1
                i=i+1
                csvfile = open("/scratch2/navudai/baltimorefiles/file"+str(i)+".csv",'wb')
                f1= csv.writer(csvfile, delimiter=',');
                         #open("/scratch2/navudai/baltimorefiles/file"+str(i)+".txt",'w') 

        f1.writerow(line)


'''
for line in f:
	line.partition(' ')
        tweetText = line.split(' ')
	#print tweetText[1]
	tDateall = tweetText[1].partition(',')
	tDate = tDateall[0]
	
        tweetDate = datetime.datetime.strptime(tDate, "%H:%M:%S-04:00")
	
	#day=tweetDate.day
	hr=tweetDate.hour
	if i is 0 or hr is not phr:
		phr=hr
		#pday=day
		i=i+1
		f1=open("/scratch2/navudai/bostonfiles/file"+str(i)+".txt",'w') 
	f1.write(line)	
'''
