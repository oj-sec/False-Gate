#!/usr/bin/env python3

# browser_driver is a utility for using Selenium to input honeypot credentials into phishing pages.

#selenium-4.8.0 
#selenium-wire-5.1.0

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class BrowserDriver:

	# Initialisation method.
	def __init__(self, target, credentials):
		# Driver options
		chrome_options = uc.ChromeOptions()

		# Class attributes		
		self.driver = uc.Chrome(options=chrome_options, seleniumwire_options={})
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
				body.click()
				body.send_keys(Keys.TAB)
				time.sleep(2)
				# Actionchains is used here because Chromedriver was not responding to Keys.ENETR
				actions = ActionChains(driver)
				actions.send_keys(Keys.ENTER)
				actions.perform()
				time.sleep(1)
				elems[0].send_keys(username)
			except:
				return 1

		try:
			elems[1].send_keys(password)
			time.sleep(1)
			elems[1].send_keys(Keys.RETURN)
			time.sleep(10)
		except:
			try:
				elems[0].send_keys(Keys.RETURN)
				time.sleep(10)
				elems[1].send_keys(username)
				elems[1].send_keys(Keys.RETURN)
				time.sleep(3)
			except:
				return 1

	# Function to handle webdriver termination.
	def close(self):

		driver = self.get_attribute("driver")
		driver.close()


	# Function to inspect the web requests made during the fuzz. 
	def inspect_requests(self):

		posts_sent = []

		driver = self.get_attribute("driver")

		for request in driver.requests:
			print(request)

		for request in driver.requests:

			if request.method == "POST":
				# omit useless Mozilla tracking POSTS
				if "mozilla.com" not in request.url:
					temp = {}
					temp['postTarget'] = request.url
					temp['postData'] = request.body
					posts_sent.append(temp)

		return posts_sent


bd = BrowserDriver("https://gateway.ipfs.io/ipfs/QmbLd37HqzS5Nid7yrwZVb3X28qYyVRtodF5U1gnBqTeC3", {'popoo@gmail.com':"weweee"})
bd.select_fuzzer()
requests_sent = bd.inspect_requests()
print(requests_sent)
bd.close()

#https://gateway.ipfs.io/ipfs/QmbLd37HqzS5Nid7yrwZVb3X28qYyVRtodF5U1gnBqTeC3
#https://gateway.ipfs.io/ipfs/QmXJ6KtWsFYkW2RDTWnw3b7mF8vecyfV4w7aQtLqjGbNN4