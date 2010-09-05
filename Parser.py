from HTMLParser import HTMLParser

class TorrentParser(HTMLParser):
    __inAtag = False
    __inBtag = False
    __addr = ""
    __dataList = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
		for attr in attrs:
			self.__inAtag = True
			self.__addr = attr[1]
	elif tag == 'b':
		self.__inBtag = True

    def handle_endtag(self, tag):
        if tag == 'a':
		self.__inAtag = False
	elif tag == 'b':
		self.__inBtag = False

    def handle_data(self,data):
        if self.__inAtag and self.__inBtag:
		self.__dataList[ data.encode("utf-8") ] = self.__addr.encode("utf-8")

    def get_data(self):
        return self.__dataList

class HomeParser(HTMLParser):
    __inTDtag = False
    __inTorrentName = False
    __inTorrentURL = False
    __inStatus = False
    __addr = ''
    __entry = []
    __dataList = []

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for attr in attrs:
		if attr[0].lower() == 'style' and attr[1].lower() == 'overflow:hidden':
                   self.__inTDtag = True
		elif attr[0].lower() == 'class' and attr[1].lower() == 'refresh':
                   self.__inStatus = True
	elif self.__inTDtag and tag == 'span':
            self.__inTorrentName = True
	elif self.__inTDtag and tag == 'a':
            self.__inTorrentURL = True
            for attr in attrs:
                   self.__addr = attr[1]

    def handle_endtag(self, tag):
        if self.__inTDtag and tag == 'td':
            self.__inTDtag = False
        if self.__inStatus and tag == 'td':
            self.__inStatus = False
	elif self.__inTDtag and tag == 'span':
            self.__inTorrentName = False
	elif self.__inTDtag and tag == 'a':
            self.__inTorrentURL = False

    def handle_data(self,data):
        if self.__inTorrentName:
            self.__entry.append(data.splitlines(False)[0])
            self.__entry.append("http://torrific.com" + self.__addr)
	elif self.__inStatus:
            self.__entry.append(data.split()[0])
            self.__dataList.append(self.__entry[:])
            self.__entry = []

    #######################
    # [ [name, url, status].....]
    #######################
    def get_data(self):
        return self.__dataList
