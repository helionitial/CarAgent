import urllib2 
from sgmllib import SGMLParser
 
# this is the Tag Attribute Checker class, a utility class
class TagAttributeChecker:
	#Find given pair of attributeName and attributeValue in a certain attributeList
	#If the pair is found, return 1, else return 0
	def checkAttribute(self, attributeList, attributeName, attributeValue):
		for attributeIter in attributeList:
			if attributeIter[0] == attributeName:
				if attributeIter[1] == attributeValue:
					return 1
		return 0

# The Craigslist Source Page Refine Manager
class CraigslistSPRM(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.machineState = 0 #0 -> finding the <span> which class = 'pl'. 1 -> finding the <a>. 2 -> ready to process next <span>
		self.processState = 0 #0 -> do not process the data, 1 -> process the data
		self.refineResultList = []
		self.tagAttributeChecker = TagAttributeChecker()
	def start_a(self, attrs):
		if self.machineState == 1:
			self.processState = 1
	def end_a(self):
		if self.machineState == 1:
			self.machineState = 2
			self.processState = 0

	def handle_data(self, text):
		if self.processState == 1:
			self.refineResultList.append(text)

	def start_span(self, attrs):
		if self.machineState == 0:
			if self.tagAttributeChecker.checkAttribute(attrs, 'class', 'pl') == 1:
				self.machineState = 1

	def end_span(self):
		if self.machineState == 2:
			self.machineState = 0
#The spider parent class, considering remove or rework on this parent class
class Spider:
	def __init__(self):
		self.webSourcePageContentList = []

#The Spider for Cragslist car section
class CraigslistSpider(Spider):
	
	def __init__(self):
		Spider.__init__(self)
		self.spiderCount = 0 #The count of spider times eg.
	#webURL is the URL of the website, dataRowAmount is the count of the row data
	#you want to spider
	def spiderWebSite(self, webURL, dataRowAmount):
		self.spiderCount = dataRowAmount / 100
		for i in range(0, self.spiderCount):
			self.webSourcePageContentList.append(urllib2.urlopen(webURL).read())

#Spider manager is the main class that is responsible for running all spider
class SpiderManager:
	def __init__(self):
		self.spiderList = []	#in later, all the spider will be added into this spider list
		self.craigSpider = CraigslistSpider() #the spider for craigslist
		self.craigSPRM = CraigslistSPRM() #considering write a CraigslistSPRM Facotry instead define this as a attribute
		self.craigURL = "https://dallas.craigslist.org/cta/" #The craigslist spider destinition URL
		self.craigDataRowAmount = 300 #The total row number needed to be spidered

		#run all the spider in the spider Manager (right now is for testing only)
	def runAllSpider(self):
		self.craigSpider.spiderWebSite(self.craigURL, self.craigDataRowAmount)
		for i in range(0, self.craigSpider.spiderCount):
			self.craigSPRM.feed(self.craigSpider.webSourcePageContentList[i])
		for item in self.craigSPRM.refineResultList:
			print item 
		print 'There are ', len(self.craigSPRM.refineResultList), 'row information spidered.'

spiderManager = SpiderManager()
spiderManager.runAllSpider()




