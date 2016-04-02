import json
import urllib, urllib2

BING_API_KEY = 'bEIR93pA4QXNENxzQDrfPH33XGxI5JC2PXTTUuo6HyM'

def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    result_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)
#First, the function prepares for connecting to Bing by preparing the URL
#that wel be requesting.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        result_per_page,
        offset,
        query)
#The function then prepares authentication, making use of your Bing API key.
    username='bEIR93pA4QXNENxzQDrfPH33XGxI5JC2PXTTUuo6HyM'

    passwword_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passwword_mgr.add_password(None, search_url, username, BING_API_KEY)

    results = []
    try:
        handler = urllib2.HTTPBasicAuthHandler(passwword_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
#We then connect to the Bing API through the command
#urllib2.urlopen(search_url). The results from the server are read and saved as a string.
        response = urllib2.urlopen(search_url).read()
#This string is then parsed into a Python dictionary object using the json Python package.
        json_response = json.loads(response)

#We loop through each of the returned results, populating a results dictionary.
#For each result, we take the title of the page, the link or URL and a short summary of each returned result.
        for result in json_response['d']['results']:
            results.append({
            'title': result['Title'],
            'link': result['Url'],
            'summary': result['Description']})
    except urllib2.URLError as e:
        print "error when querying the bing API", e
#The dictionary is returned by the function.
    return results

def main():

    query = raw_input("please enter a query: ")
    results = run_query(query)
    rank = 1

    for result in results:

        print "Rank {0}".format(rank)
        print result['title']
        print result['link']
        print

        rank += 1

if __name__ == '__main__':
    main()











