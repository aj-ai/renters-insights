import requests
import os
import pickle
import json

# NORTH STAR: get data to create a "deal score" for each apartment
# In comparison to expected price, a score of 1-100 should be assigned for each apartment given bed, bath, sqft, amenities, and description.

# Need:
# Listings API (Realty Mole)
# Mapping of Longitude/Latitude to neighborhood
# Geolocator API (zip -> long/lat and vice versa)
# API to find positioning of train station
# API to find positioning of other places nearby
# Find pricing of other non-listed apartments and what they sold for

with open('../credentials/realty_mole_api.json') as realty_mole_cred_file:
	realty_mole_creds = json.load(realty_mole_cred_file)

	realty_mole_headers = {
		"X-RapidAPI-Key": realty_mole_creds['api_key'],
		"X-RapidAPI-Host": realty_mole_creds['api_host']
	}

def check_num_executes():
	"""
	Checks to see if executing a call to the API is still free. (You get 50 executes per month)
	"""
	with open('../config/count_api_executes.pkl', 'rb') as f:
		num_exe = pickle.load(f)

	if num_exe >= 50:
		print("WARNING - execute stopped because monthly number of API calls reached")
		raise Exception
	elif num_exe >= 40:
		print(f"WARNING - you are reaching the number of executes allowed per month. You are currently at {num_exe}")

def increment_num_executes():
	"""
	Increments the number of executes to make sure that we don't go over the allotted amount per month.
	"""

	with open('../config/count_api_executes.pkl', 'rb') as f:
		num_exe = pickle.load(f)

	num_exe += 1

	with open('../config/count_api_executes.pkl', 'wb') as f:
		pickle.dump(num_exe, f)

def print_num_executes():
	"""
	Prints the number of executes that have been made.
	"""

	with open('../config/count_api_executes.pkl', 'rb') as f:
		print(f"Number of times that the API has been called this month: {pickle.load(f)}")

def get_records_by_address(address: str, headers=realty_mole_headers):
	check_num_executes()

	url = "https://realty-mole-property-api.p.rapidapi.com/properties"

	querystring = {"address": address}

	response = requests.request("GET", url, headers=headers, params=querystring)
	increment_num_executes()

	return response

def get_rent_agg_by_zip(zip: int, headers=realty_mole_headers):
	check_num_executes()

	# Assert that zip is a valid format for a zip code
	try:
		assert len(str(zip)) == 5
	except AssertionError as msg:
		print(f"ERROR: Zip code {zip} is not a valid zip code")

	url = f"https://realty-mole-property-api.p.rapidapi.com/zipCodes/{zip}"

	response = requests.request("GET", url, headers=headers)
	increment_num_executes()

	return response

def get_listings(city: str, state: str, latitude, longitude, radius, bedrooms, bathrooms=None, limit=10):
	"""
	Get rental listings for a given city, state, latitude, longitude, radius
	For certain apartments with a number of bedrooms, bathrooms, and limit
	"""
	# TODO - find a way to get longitude and latitude by zip code
	# TODO - for each listing, you want to find proximity to train station
	# TODO - for each listing, you want to find historical prices
	pass

if __name__ == "__main__":
	zip = input("Enter the zipcode you would like to get rent aggregates for... \n")

	print(f"Getting data for zip code {zip}: ")
	response = get_rent_agg_by_zip(zip=zip)

	with open(f"../data/by_zip/rent_agg_by_zip_{zip}.pkl", "wb") as f:
		pickle.dump(response, f)

	print_num_executes()
