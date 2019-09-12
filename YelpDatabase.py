import pygsheets
import pandas as pd
import requests
import json

# authorization, enter your own file name
gc = pygsheets.authorize(service_file='/Users/Andrew Huh/Documents/SearchEngine/creds.json')

# Create empty dataframe
df = pd.DataFrame()

#E nter your API Key here
api_key=''

headers = {'Authorization': 'Bearer %s' % api_key}

# Yelp API URL
url = 'https://api.yelp.com/v3/businesses/search'

# Enter categories or specific business names that you'd like to search
categories = ['']

# Enter a text file of cities or zip codes that you wish to search
f = open('MontgomeryCoZipCodes.txt', "r")
locations = f.readlines()
# Close the file after reading the lines.
f.close()

# Various categories
BusinessName = []
Category = []
Address = []
ZipCode = []
City = []
Rating = []
ReviewCount =[]
PhoneNumber = []
URL = []
YelpID = []

for category in categories:
    for location in locations:
        # In the dictionary, term can take either categories or specific business names, it's up to you!
        params = {'term': category, 'location': location}

        req = requests.get(url, params=params, headers=headers)

        parsed = json.loads(req.text)

        businesses = parsed["businesses"]

        # Adds all appropriate information, can be changed if you want different information
        for business in businesses:
            BusinessName.append(business["name"])
            Category.append("".join(business["categories"][0]["title"]))
            Address.append("".join(business["location"]["display_address"]))
            ZipCode.append(business["location"]["zip_code"])
            City.append(business["location"]["city"])
            Rating.append(business["rating"])
            ReviewCount.append(business["review_count"])
            PhoneNumber.append(business["display_phone"])
            URL.append(business["url"])
            YelpID.append(business["id"])

# Create a column
df['BusinessName'] = BusinessName
df['Category'] = Category
df['Address'] = Address
df['ZipCode'] = ZipCode
df['City'] = City
df['Rating'] = Rating
df['Review Count'] = ReviewCount
df['PhoneNumber'] = PhoneNumber
df['URL'] = URL
df['YelpID'] = YelpID


#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('YelpData')

#select the first worksheet
wks = sh[0]

#update the first sheet with df
wks.set_dataframe(df,(1,1))

