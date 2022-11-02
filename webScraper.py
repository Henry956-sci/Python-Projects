import re

# The following function reads content of the web page at a given url 
# and copy it to a given outout File

import socket

def readWebPage(url, outputFile="webContent.html"):

	# Construct socket object
	mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# check the format of teh url and extract host name
	hostMatch = re.search("http[s]?:\/\/((www\.)?(\S+\.)+\S+)", url)
	if hostMatch == None:
		print("Invalid url")
		return
	host = hostMatch.groups()[0]
	port = 80

	# Establish the connection
	print("connecting ", host, ": ", port)
	mysock.connect((host, port))

	# generate and submit http command
	cmd = 'GET ' + url + ' HTTP/1.0\r\n\r\n'
	cmd = cmd.encode()
	mysock.send(cmd)

	# create the output fiele 
	try:
		wfhand = open(outputFile, 'w')
	except:
		print("Unable to open file.")
		exit()

	while True:
		data = mysock.recv(512)
		if (len(data) < 1):
				break
		# Try different ecnoding
		try:
			decoded_data = data.decode(encoding = "UTF-8")
		except:
			try:
				decoded_data = data.decode(encoding = "UTF-16")
			except:
				try:
					decoded_data = data.decode(encoding = "UTF-32")
				except:
					decoded_data = "decoding error"
		print(decoded_data)
		try:
			wfhand.write(decoded_data)
		except:
			continue

	mysock.close()
	wfhand.close()


# The following function attempts finds all web links embedded in 
# the web page at the given url and write them to a file with the given name

import urllib.request, urllib.parse, urllib.error

def extractLinks(url, linkFile, contentFile="webContent.html"):
	#initiates list to be returned by function
	listLink = []
	#opens the url to be searched
	rfhand = urllib.request.urlopen(url)

	try:
		#attempts to open the files that are to be written to
		wfhand = open(linkFile, 'w')
		wfhand1 = open(contentFile, 'w')
	except:
		#otherwise, gives error and exits program
		print("Unable to open file.")
		exit()

	#goes through every line of the webpage
	for line in rfhand:
		try:
			#attempts to decode using UTF-8
			decoded_line = line.decode(encoding = "UTF-8")
		except:
			try:
				#otherwise, attempts to decode using UTF-16
				decoded_line = line.decode(encoding = "UTF-16")
			except:
				try:
					#otherwise, attempts to decode using UTF-32
					decoded_line = line.decode(encoding = "UTF-32")
				except:
					#if all else fails, gives a decoding error
					decoded_line = "decoding error"
		#print(decoded_line)
		try:
			#attempts to write the decoded line to the content file
			wfhand1.write(decoded_line)
		except:
			#otherwise, it starts the loop again with the next iteration
			continue
		#searches for a link in the given format
		linkList = re.findall('href="((https?:)?\/\/(\S+\.)+\S+)"', decoded_line)
		#if the array is empty, no links were found
		if linkList == []:
			#so it starts the loop again with the next iteration
			continue
		#otherwise, it goes through the links in the list
		for link in linkList:
			try:
				#if the link is not already in the list, it adds the link to the list
				if link[0] not in listLink:
					if link[0] != url:
						newLink = str(link[0])
						wfhand.write(newLink + "\n")
						listLink.append(newLink)
			except:
				#otherwise, starts the loop again with the next iteration
				continue
	
	#closes all files and returns the list
	rfhand.close()
	wfhand.close()
	wfhand1.close()
	return listLink


# The following are the chosen URLs

#url = "https://store.steampowered.com"
#url = "https://www.tesla.com"
#url = "https://www.google.com"
#url = "https://www.nbcnews.com"
url = "https://www.instagram.com"

#initiates the list to be read
listofLinks = [url]

#readWebPage(listofLinks[0], "webContent.html")
print('ORIGINAL LIST: ', listofLinks)
#initiates counter to 0
i = 0
#stores the beginning size of the list in origSize
origSize = len(listofLinks)
while True:
	#prints the current number of iteration
	print(i)
	try:
		#calls the function to search the current url, and searches it for more urls. stores the new urls in newLinks. In the case that it fails because of error 403, it goes to except
		newlinks = extractLinks(listofLinks[i], "weblinks.txt")
	except:
		#if i has reached the origSize
		if i == origSize:
			#stores the number of iterations in count
			count = i
			#ends the loop
			print('PROGRAM EXECUTED', i, ' TIMES. LOOP TERMINATED')
			break
		#increments i by 1
		i = i + 1
		continue
	#goes through the list of new links
	for link in newlinks:
		#adds every new link to the original list
		listofLinks.append(link)
	#converts list to set to get rid of identical entries
	listSet = set(listofLinks)
	#reverts the set back to a list
	listofLinks = list(listSet)
	#newSize is the new size of the original list that now contains the new links as well
	newSize = len(listofLinks)

	#if i reaches the number in origSize
	if i == origSize:
		#if i is less than new size
		if i < newSize:
			#then it makes origSize be the newSize
			origSize = newSize
		else:
			#else, it means that the list has not grown, thus the list can end
			count = i
			print('PROGRAM EXECUTED', i, ' TIMES. LOOP TERMINATED')
			break

	#increments i by 1
	i = i + 1

	#if iterations reach 500, it is assumed infinite
	if i == 500:
		print('PROGRAM HAS EXECUTED AT LEAST', i,' TIMES, CAN BE ASSUMED INFINITE. LOOP TERMINATED.')
		count = i
		break

#writes results to files
results = open('Instagram day 2', 'w')
results.write('INSTAGRAM RESULTS' + '\n')
for i in range(len(listofLinks)):
	results.write(listofLinks[i] + '\n')