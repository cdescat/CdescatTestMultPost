# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import csv

class MultipostingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass






class OfferItem(scrapy.Item):
	offer = scrapy.Field()
	title = scrapy.Field()
	country = scrapy.Field()
	location_name = scrapy.Field()
	postal_code = scrapy.Field()
	education_level = scrapy.Field()
	experience_level = scrapy.Field()
	contract_type = scrapy.Field()
	job_description = scrapy.Field()
	profile_description = scrapy.Field()

	# Write item as a row into the CSV file attached to c writer.

	def writeRowCSV(self, c):
		c.writerow([
			self['offer'],
			self['title'],
			self['country'],
			self['location_name'],
			self['postal_code'],
			self['education_level'],
			self['experience_level'],
			self['contract_type'],
			self['job_description'],
			self['profile_description']
		])

# Write a header row for OfferItem keys into the CSV file attached to c writer.

def writeOfferItemHeaderRowCSV(c):
	c.writerow([
		"offer",
		"title",
		"country",
		"location_name",
		"postal_code",
		"education_level",
		"experience_level",
		"contract_type",
		"job_description",
		"profile_description"
	])
