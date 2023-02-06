#!/usr/bin/env python3

# browser_driver is a utility for using Selenium to input honeypot credentials into phishing pages.

#selenium-4.8.0 
#selenium-wire-5.1.0

import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

class BrowserDriver:

	# Initialisation method.
	def __init__(self, target, credentials):
		# Driver options
		chrome_options = uc.ChromeOptions()
		chrome_options.add_argument("--incognito")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-setuid-sandbox")
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--headless")


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

	# Function to select and execute the fuzzing routine.
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

		# Insert additional fuzzers here with appropriate condition
		self.basic_page_engagement_routine()
		return "basic-page-engagement"


	# Function to preform a generic engagement routine against the target page to attempt to fuzz form fields
	# Works by trying to tab + enter through 0-1 buffer elements and then a login screen.
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
		del driver.requests
		driver.close()


	# Function to inspect the web requests made during the fuzz. 
	def inspect_requests(self):

		posts_sent = []

		driver = self.get_attribute("driver")

		for request in driver.requests:

			if request.method == "POST":
				# omit useless Google tracking POSTS
				if "google-analytics.com" not in request.url and "update.googleapis.com" not in request.url:
					temp = {}
					temp['postTarget'] = request.url
					temp['postData'] = str(request.body)
					posts_sent.append(temp)

		return posts_sent

	# Class entrypoint and main execution handler
	def start(self):

		credentials = self.get_attribute("credentials")
		target = self.get_attribute("target")

		try:
			fuzzer = self.select_fuzzer()
			requests_sent = self.inspect_requests()

			if requests_sent:
				formatted_return = {}
				formatted_return['targetUrl'] = target
				formatted_return['credentialsUsed'] = credentials
				formatted_return['engagementRoutine'] = fuzzer
				formatted_return['postRequestsTriggered'] = requests_sent

				self.close()
				return formatted_return

			else:
				self.close()

		except:
			self.close()
			return

