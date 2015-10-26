import scrapy
from MultiPosting.items import OfferItem
from MultiPosting.items import writeOfferItemHeaderRowCSV
import json
import csv

# Another version of OfferSpider, starting from the classic user offer visualisation page.
# This one is better suited for sites that are not going to be modified often, for example clients that do not have any real development team.
# Plus: It prevents the crawl to be broke if the feeding URL was to change.
# Weak points:
# -Changes in the naming, especially the key 'feed' in options{"" = "",..., "" = ""} sent to MPCorpo.recruitment.init
# -Direct changes in the MPCorpo.recruitment.init naming
# -Modifications of the javascript position inside the DOM, and CSS namings can easily affect the xpath selectors

# Changes to do : Try using defined CSV writers from scrapy if possible
# Adding a method for the JSON offer to item utf8 encoding

class Offer2Spider(scrapy.Spider):
	name = "offer2"
	allowed_domains = ["multiposting.fr"]
	start_urls = [
		"http://multiposting.fr/fr/a_propos/recrutement"
	]


	# Extraction of javascript code from source code via xpath selector
	# regexp for MPCorpo.recruitment.init({'feed': '/URL/'});
	# joining current URL and /URL/ (working with both absolute and relative URL)
	# new scrapy.Request done with this url, with parseJSON as a callback. 

	def parse(self, response):
		url = response.xpath('//div[@id="wrapper"]/script')[1].re("MPCorpo.recruitment.init\({\'feed\': \'((https?:\/\/)?(([\da-z\.-]+)\.([a-z\.]{2,6}))?([\/\w \.-]*)*\/?)\'}\);")[0]
		url = response.urljoin(url)
		yield scrapy.Request(url, callback=self.parseJSON)

	# Response.body is loaded with json.loads
	# if extracted data exist:
	# a csv.writer is instantiated
	# header row containing column names is writen to offer.csv
	# each offer contained in the loaded JSON file is:
	# encoded to utf8 standard and stocked in an OfferItem
	# (((which is not really used here, but would permit to export
	# to different formats/files/database, and helps to keep the code clear)))
	# writen attribute by attribute to offer.csv as a single row.

	def parseJSON(self, response):
		data = json.loads(response.body)
		if data and data['offers'] and len(data['offers']) != 0:
			c = csv.writer(open("offers2.csv", "wb"))
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