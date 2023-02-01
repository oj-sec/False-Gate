#!/usr/bin/env python3

#selenium-4.8.0 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class BrowserDriver:

	# Initialisation method.
	def __init__(self, target, credentials):
		# Driver options
		profile = webdriver.FirefoxProfile()
		profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")

		# Class attributes		
		self.driver = webdriver.Firefox(firefox_profile=profile)
		self.driver.set_window_size(1366,768)
		self.target = target
		self.credentials = credentials

	# Getter method for value of class attributes
	def get_attribute(self, attribute):
		attributes = self.__dict__
		try:
			return attributes[attribute]
		except:
			return

	# Function to select the fuzzing routine to use on the target.
	def select_fuzzer(self):
		driver = self.get_attribute("driver")
		target = self.get_attribute("target")

		try:	
			driver.get(target)
			# Padding time to allow dynamic elements to load
			time.sleep(3)
		except:
			return 1

		# Count form elements
		elems = driver.find_elements(By.TAG_NAME, "input")

		if len(elems) == 2:
			self.basic_page_engagement_routine()



	# Function to preform a generic engagement routine against the target page to attempt to fuzz form fields.
	def basic_page_engagement_routine(self):
		driver = self.get_attribute("driver")
		(username, password), = self.get_attribute("credentials").items()

		elems = driver.find_elements(By.TAG_NAME, "input")

		try:
			elems[0].send_keys(username)
		except:
			try:
				# Select the body so we can try to tab + return a button
				body = driver.find_element(By.TAG_NAME, "body")
				body.send_keys(Keys.TAB)
				body.send_keys(Keys.RETURN)

				elems[0].send_keys(username)
			except:
				return 1

		try:
			elems[1].send_keys(password)
		except:
			try:
				elems[0].send_keys(Keys.RETURN)
				time.sleep(10)
				elems[1].send_keys(username)
				elems[1].send_keys(Keys.RETURN)
			except:
				return 1

	# Function to handle webdriver termination.
	def close(self):

		driver = self.get_attribute("driver")
		driver.close()


bd = BrowserDriver("https://gateway.ipfs.io/ipfs/QmXJ6KtWsFYkW2RDTWnw3b7mF8vecyfV4w7aQtLqjGbNN4", {'popoo@gmail.com':"weweee"})
bd.select_fuzzer()
bd.close()