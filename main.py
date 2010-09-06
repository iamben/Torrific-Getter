# -*- coding: utf-8 -*-
import sys, os, getpass, urllib, urllib2, cookielib
import helper
import Parser

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: getFiles.py topLevelDir\n")
	exit(1)


    ##############################
    #init
    ##############################
    DirList = []
    #RawData = sys.stdin.read();
    TorrentParser = Parser.TorrentParser()
    HomeParser = Parser.HomeParser()
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cj ) )
    urllib2.install_opener( opener )

    ##############################
    #login, get torrent info for parsing
    ##############################
    loginName = raw_input('Login Name: ')
    passwd = getpass.getpass("Torrific: %s's password:" % loginName)
    values = { "email":loginName, "password":passwd }
    data = urllib.urlencode(values)
    loginReq = urllib2.Request( 'http://torrific.com/login/', data )
    login = urllib2.urlopen(loginReq)
    HomeParser.feed( login.read().decode("utf-8") )

    ###############################
    #show torrents in this account, prompt for selection
    ###############################
    tor = HomeParser.get_data()
    print "Available torrents are marked in green."
    while True:
	for i,t in enumerate(tor):
            if t[2] == 'available':
		print i,"[1;32m"+t[0]+"[m"
            else:
		print i,"[1;31m"+t[0]+"[m","[1;35m"+t[2]+"[m"
	selected = int(raw_input("Select the torrent: "))

	if tor[selected][2] != 'available':
            print "Not available."
	else:
            break;

    ######################################
    #open the url
    ######################################
    torrentInfo = urllib2.urlopen(tor[selected][1])
    RawData = torrentInfo.read()


    ##############################
    #feed the parser
    ##############################
    TorrentParser.feed( RawData.decode( "utf-8" ) )
    fileAddrPair = TorrentParser.get_data()
    for filePath in fileAddrPair:
	path = filePath.decode("utf-8").rsplit( "/", 1 )
	if len(path) == 1:
            continue
        DirList.append(path[0].encode("utf-8"))

    ##############################
    #now create the directory tree
    ##############################
    if len(DirList) == 0:
        os.mkdir(sys.argv[1]) #create tld if no sub dirs
    else:
	DirList = list(set(DirList))[:];
	DirList.sort() #sort the list so the leaf dir would be created later

	for subDir in DirList:
            dirs = sys.argv[1] + "/" + subDir
            print "Making directory: %s" % ( dirs )
            os.makedirs( dirs, 0755 )

    ##############################
    #now fetch the file
    ##############################
    for filePath in fileAddrPair:
        print filePath, fileAddrPair[filePath]
	fileStream = urllib2.urlopen(fileAddrPair[filePath])
	helper.chunk_read( fileStream, sys.argv[1]+"/"+filePath, report_hook=helper.chunk_report )

if __name__ == '__main__':
    main()
