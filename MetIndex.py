
# NOTES: When using this program, you have to make some slight alterations manually to the .txt file. First, add "--start of poem--" just before line 1.
# Also, since debugging every special case in the line numbers would be a big challenge, I included code to note where the program's internal representation of line number
# contrasts with what Luke's book says. Just go into the text file and fix it manually. Also make sure to manually check lines that look like 224a, or other weird ones
# 

import sys
import pathlib
import csv
import pickle
import re

class BigOvidIndex:
	def __init__(self, ovidIndexFilename, ovidBookFilenames):
		self.ovidIndexFilename = ovidIndexFilename
		self.ovidBookFilenames = ovidBookFilenames
		# Opens and loads the index data stored in a pickled .txt file
		try:
			with open(ovidIndexFilename, 'rb') as handle:
				self.namesDict = pickle.load(handle)
		# Creates the pickle file if it doesn't already exist
		except:
			self.namesDict = {}
			self.update()
		
	# Save the current index dictionary into a pickle file
	def update(self):

		with open(self.ovidIndexFilename, 'wb') as handle:
			pickle.dump(self.namesDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
		

	def findName(self, name):
		
		allInstancesOfName = {name:[]}
		romanNumerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
		rnCount = 0

		# Look at each book of the poem in turn, and add a list of line numbers where the name appears to the index.
		for filename in self.ovidBookFilenames:
			print("Book " + romanNumerals[rnCount] + ":")
			# Create a local index for the book in question
			ovidBookIndex = OvidBookIndex(filename)
			ovidBookIndex.addName(name)
			#return dictionary containing all instances of a name in the book with line numbers
			bookIndex = ovidBookIndex.indexDictionary() 

			#If a name does not appear in the book, don't print that book's roman numeral in the index
			if not bookIndex[name]:
				print(name + " not in", filename.split('/')[-1])
				print()
				print()
				rnCount +=1
				continue
			
			bookIndex[name][0] = romanNumerals[rnCount] + '.' + str(bookIndex[name][0]) #note that all entries in the list except first and last are integers
			rnCount +=1
			print()
			print()

			#Add a semicolon to the end of the list for nice formatting
			if len(bookIndex[name]) > 0:
				bookIndex[name][-1] = str(bookIndex[name][-1]) + ';'

			allInstancesOfName[name].append(bookIndex[name])

		if allInstancesOfName[name]:
			self.namesDict.update({name: allInstancesOfName[name]})
			print()
			print("Instances of \'" + name + "\':")
			print(self.namesDict[name])

	# Removes a name from the index (e.g. when you've searched for and added a misspelled name)
	def deleteName(self, name = 0):
		if name in self.namesDict:
			self.namesDict.pop(name)
			print()
			print("\'" + name + "\' deleted from Index.")

	# Write index.txt with names in alphabetical order
	def makeIndex(self):
		index = open("/Users/truszala/Documents/python!/Metamorphoses/index.txt", "w")
		sortedDictTuple = sorted(self.namesDict.items())

		# Format the index beautifully
		for item in sortedDictTuple:
			lineNumbers = str(item[1]).replace('\'', '').replace("],", '').replace("[", '').replace("]", '')
			index.write(str(item[0]) + ":" + '\n' + lineNumbers)
			index.write('\n' + '\n')

		print()
		print("Index Updated.")


# Object to represent Luke's book
class OvidBookIndex:
	def __init__(self, fullFilename):
		self.file = fullFilename
		self.indexDict = {}
	
	# find all instances of the given name in the book, and add the line numbers to the local index.
	def addName(self, name):
		listOfLineNumbersForThisName = []
		f = open(self.file, 'r')
		
		# Get to the beginning of the poem
		haveWeReachedThePoem = False # flag variable to help us find the first line of the poem, initially false
		while haveWeReachedThePoem == False:
			l = f.readline()
			if "--start of poem--" in l:
				haveWeReachedThePoem = True
		

		lineNumber = 1
		for eachLine in f:
			regEx = name + '\\W'
			if re.search(regEx, eachLine, re.IGNORECASE):
			#if name in eachLine:
				listOfLineNumbersForThisName.append(lineNumber)
				print(lineNumber, eachLine)

			#This part of the code helps with minor manual preformatting and checking line numbering errors.
			if not eachLine.isspace(): #skipping blank lines, i.e. section breaks
				if eachLine[-3].isdigit(): #checking to see if the end of the line contains a number. Note that this won't work for numbers like 544a* in book 1. Not sure what do do about that. Maybe find those lines individually and index them.
					lineNumberInBook = int(eachLine.split()[-1]) #gets the line number
					if lineNumber != lineNumberInBook:
						print("lineNumber = ", lineNumber, "; lineNumberInBook = ", lineNumberInBook) #because this situation won't happen super often, and could be gnarly, we'll do this by hand, i.e.: Edit the .txt file.
						print(eachLine)
				lineNumber += 1
			# 'TRANSLATION NOTES' signals the end of the poem in each file.
			if "TRANSLATION NOTES" in eachLine:
				break

		self.indexDict.update({name: listOfLineNumbersForThisName})

	def indexDictionary(self):
		return self.indexDict






def main():

	directory = str(pathlib.Path(__file__).parent.resolve()) + '/'
	# ovidIndexFilename refers to the file where pickle stores the bigOvidIndex data structure.
	ovidIndexFilename = directory + "OvidIndexStorage.txt"
	bookDirectory = directory + 'books/'
	ovidBookFilenames = [bookDirectory + "LiberPrimus.txt", bookDirectory + "LiberSecundus.txt", bookDirectory + "LiberTertius.txt", bookDirectory + "LiberQuartus.txt", 
						 bookDirectory + "LiberQuintus.txt", bookDirectory + "LiberSextus.txt", bookDirectory + "LiberSeptimus.txt", bookDirectory + "LiberOctauus.txt",
						 bookDirectory + "LiberNonus.txt", bookDirectory + "LiberDecimus.txt", bookDirectory + "LiberUndecimus.txt", bookDirectory + "LiberDuodecimus.txt", 
						 bookDirectory + "LiberTertiusDecimus.txt", bookDirectory + "LiberQuartusDecimus.txt", bookDirectory + "LiberQuintusDecimus.txt"]
	#Load saved index data (e.g. from a previous work session)
	bigOvidIndex = BigOvidIndex(ovidIndexFilename, ovidBookFilenames)
	
###########################################################################################################################################################################

#																			LUKE LOOK HERE!

# INSTRUCTIONS: Use the findName() command below to add names to the index, with information on every place that name appears. 
# -Make sure to put the name between single or double quotation marks.
# -If you need to search for something with an apostrophe, copy/paste this charater: ’    (Typing a single quotation mark won't do the trick.)
# -Also, if you try to findName() a name which has already been added, nothing bad will happen. :)

# Names can be searched from the command line, e.g.:
#	"python3 MetIndex.py Jove" will add all instances of 'Jove' to the index
#	"python3 MetIndex.py -rm Jove" will remove the entry for 'Jove' from the index
	if len(sys.argv) > 1:
		if sys.argv[1] == '-rm':
			bigOvidIndex.deleteName(sys.argv[2])
		else:
			bigOvidIndex.findName(sys.argv[1])
	else:
	# example:
	# 	bigOvidIndex.findName('Jove')
		bigOvidIndex.findName('Jove')

	# Use deleteName() if you accidentally mispelled a name and need to remove it from the index.
	# example:
	#	bigOvidIndex.deleteName('duck')
		bigOvidIndex.deleteName('')


###########################################################################################################################################################################

	bigOvidIndex.makeIndex()
	bigOvidIndex.update()

if __name__ == "__main__":
	main()











