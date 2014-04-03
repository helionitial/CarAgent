import urllib2
from sgmllib import SGMLParser
 

class TagAttributeChecker:
	#Find given pair of attributeName and attributeValue in a certain attributeList
	#If the pair is found, return 1, else return 0
	def checkAttribute(self, attributeList, attributeName, attributeValue):
		for attributeIter in attributeList:
			if attributeIter[0] == attributeName:
				if attributeIter[1] == attributeValue:
					return 1
		return 0

class CraigslistCarFinderTest1(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.machineState = 0 #0 -> finding the <span> which class = 'pl'. 1 -> finding the <a>. 2 -> ready to process next <span>
		self.processState = 0 #0 -> do not process the data, 1 -> process the data
		self.carList = []
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
			self.carList.append(text)

	def start_span(self, attrs):
		if self.machineState == 0:
			if self.tagAttributeChecker.checkAttribute(attrs, 'class', 'pl') == 1:
				self.machineState = 1

	def end_span(self):
		if self.machineState == 2:
			self.machineState = 0

content = urllib2.urlopen('https://dallas.craigslist.org/cta/').read()
file = open('SourceCode', 'w')
file.write(content)
listResult = CraigslistCarFinderTest1()
listResult.feed(content)
for item in listResult.carList:
	#print item.decode('gbk').encode('utf8')
	print item
print  '\nThere are ', len(listResult.carList), 'items in result'



