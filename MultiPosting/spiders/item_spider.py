import scrapy
from MultiPosting.items import OfferItem
from MultiPosting.items import writeOfferItemHeaderRowCSV
import json
import csv

# First version OfferSpider, starting directly from the feeding URL.
# This one is better suited for sites that are going to be updated often, and have a stable feeding URL.
# Plus: It can only broke if the feeding URL is changed, or if the feeding method/format is.
# Weak points:
# -Feeding URL change
# -Feeding format change
# -Feeding method change

# Changes to do : Try using defined CSV writers from scrapy if possible
# Adding a method for the JSON offer to item utf8 encoding

class OfferSpider(scrapy.Spider):
	name = "offer"
	allowed_domains = ["multiposting.fr"]
	start_urls = [
		"http://multiposting.fr/fr/get-job-list"
	]

	# Response.body is loaded with json.loads
	# if extracted data exist:
	# a csv.writer is instantiated
	# header row containing column names is writen to offer.csv
	# each offer contained in the loaded JSON file is:
	# encoded to utf8 standard and stocked in an OfferItem
	# (((which is not really used here, but would permit to export
	# to different formats/files/database, and helps to keep the code clear)))
	# writen attribute by attribute to offer.csv as a single row.

	def parse(self, response):
		data = json.loads(response.body)
		if data and data['offers'] and len(data['offers']) != 0:
			c = csv.writer(open("offers.csv", "wb"))
			writeOfferItemHeaderRowCSV(c)
			for offer in data['offers']:
				item = OfferItem()
				item['offer'] = offer['id']
				item['title'] = offer['title'].encode('utf8')
				item['country']= offer['country'].encode('utf8')
				item['location_name']= offer['city'].encode('utf8')
				item['postal_code']= offer['postal_code'].encode('utf8')
				item['education_level']= offer['study_level'].encode('utf8')
				item['experience_level']= offer['experience'].encode('utf8')
				item['contract_type']= offer['contract_type'].encode('utf8')
				item['job_description']= offer['description'].encode('utf8')
				item['profile_description']= offer['requested_profile'].encode('utf8')
				item.writeRowCSV(c)
