#!/usr/bin/env python
# This file is copyright 2010 by Greg Hellings, and you may freely
# use or distribute this file to your heart's content, for any purpose
# whatsoever.  Realize that no warranty or responsibility for the use
# of this program lies with the aforementioned copyright holder.  You
# use or believe in the functionality of this program at your own
# peril.

from PyQt4 import QtWebKit, QtCore, QtGui

class MakeMyScreenshot(QtGui.QWidget):
	'''I will take a screen shot, save it to a file, and then
	give you all a whole bunch of fun and lols and stuff.'''
	def __init__(self, myList):
		# Pay homage to our parents
		QtGui.QMainWindow.__init__(self, None)
		
		# Our data
		self.myList = myList
		
		# How big are we going to be?
		self.setGeometry(100, 100, 1024, 768)
		
		# This is the area we want to render
		self.region = QtGui.QRegion(QtCore.QRect(0, 0, 1920, 1200))
		
		# The "view" that we will be displaying each page in
		self.view = QtWebKit.QWebView(None)
		self.view.setGeometry(0, 0, 1920, 1200)

		# This is where feedback will be shown
		self.table = QtGui.QTableWidget(len(myList), 3, None)
		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.table)
		self.setLayout(layout)
		# Table headers
		self.setupTable()
		
		# This will perform work once the page is loaded
		self.view.connect(self.view, QtCore.SIGNAL('loadFinished(bool)'), self.loaded)
		
		# This is some stuff for hopefully saving the images
		self.image = QtGui.QImage(1920, 1200, QtGui.QImage.Format_RGB32)
		
		# Now we tell the frame to load the page and all that jazz
		self.loadNext()
	
	def loading(self, blah):
		print blah
	
	def loadStart(self):
		print self.current
	
	def loaded(self, status):
		# Shortcut things if the page isn't actually loaded
		if not status:
			self.feedback('icons/error.png', 2)
			self.view.stop()
			print str(status)
			# Now, create a new one, I suppose?
			#self.view = QtWebKit.QWebView(None)
			#self.view.setGeometry(0, 0, 1920, 1200)
		else:
			# This is the HTML frame that holds our rendered site
			frame = self.view.page().mainFrame()
			
			# We construct a painter object that will hold the image we save
			painter = QtGui.QPainter(self.image)
			frame.render(painter, self.region)
			
			# We have to save the results out to a file
			self.image.save(self.filename)
			
			# If everything was successful
			self.feedback('icons/success.png')
		# Load the next one in the list
		self.loadNext()
	
	def loadNext(self):
		next = self.myList.pop(0)
		if next:
			# Load the next URL
			self.filename = next[1]
			self.current  = next[0]
			self.view.load(QtCore.QUrl(self.current))
			# User feedback
			self.feedback('icons/working.png')
		else:
			self.close()
	
	def feedback(self, text, column=2):
		# Create a new row
		newRow = self.table.rowCount() - len(self.myList) - 1
		# Add our feedback to it
		widget = QtGui.QTableWidgetItem(QtGui.QIcon(text), '')
		self.table.setItem(newRow, column, widget)
	
	def setupTable(self):
		'''This will just setup the table that gives us feedback when the
		user wants to know what is going on behind the scenes.  There are even some
		times when I want to know what is going on back there that I can't really tell,
		so this is the next best thing.  Pretty pictures and all.'''
		# First we setup the headers for the table
		headers = QtCore.QStringList()
		headers.append('Site')
		headers.append('Filename')
		headers.append('Status')
		self.table.setHorizontalHeaderLabels(headers)
		# Then we set column widths for the table
		self.table.setColumnWidth(0, 400)
		self.table.setColumnWidth(1, 400)
		self.table.setColumnWidth(2, 100)
		# Next we populate the table
		row = 0
		for site in self.myList:
			# Create holder widgets
			sname = QtGui.QTableWidgetItem(site[0])
			fname = QtGui.QTableWidgetItem(site[1])
			ricon = QtGui.QTableWidgetItem(QtGui.QIcon('icons/loading.png'), '')
			# Preload them into the table
			self.table.setItem(row, 0, sname)
			self.table.setItem(row, 1, fname)
			self.table.setItem(row, 2, ricon)
			# Increment!
			row += 1

import fileinput, sys

app = QtGui.QApplication(sys.argv)
myList = []

for url in fileinput.input():
	saneURL = url.strip()
	# Don't bother if the line is empty
	if saneURL == '': continue
	# Sanitize for a filename
	filename = 'images/' + saneURL.replace('.', '') + '.jpg'
	# Save for later
	myList.append(('http://' + saneURL, filename))

# Now we take the screenshots
shots = MakeMyScreenshot(myList)
shots.show()

# And wait for everything to be done
sys.exit(app.exec_())