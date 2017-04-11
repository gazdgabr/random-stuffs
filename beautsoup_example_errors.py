from bs4 import BeautifulSoup
import requests
import json

## THERE ARE SEVERAL ERRORS (5, but you may see more than 5 if you correct one and introduce another!) IN THIS FILE.

## Try to find and correct them by debugging this code!

# We've provided a good version of this cache file on Canvas in case you hit the web too many times and still want to try this... 
# but this version of the code wouldn't cache anything correctly anyway, till you fix it!

# Later, we'll provide a solution -- a fixed version, and go over what's wrong.

## HINT: Will be useful to print stuff out, see what it is, what's going on... this is a frustrating process! but it's 
# important practice.

CACHE_FNAME = "samplebs.json" 
try:
	f = open(CACHE_FNAME,'r')
	fstr = f.read()
	CACHE_DICTION = json.loads(fstr)
	f.close()

except:
	CACHE_DICTION = {}

def get_articles_umich():
	base_url = "http://umich.edu/"
	unique_ident = "umich_articledata_beautifulsoup"

	if unique_ident in CACHE_DICTION:
		print("Using cache\n")
		article_html_tups = CACHE_DICTION[unique_ident]
	else:
		print("Getting new data\n")
		umich_resp = requests.get(base_url).text
		soup = BeautifulSoup(umich_resp, "html.parser")
		
		sub_div = soup.find("div",{"id":"in-the-news"})
		news_articles_set = sub_div.find("ul",{"class":"news-items"})
		pe_articles_set = sub_div.find("ul",{"class":"pe-items"})
		news_links = news_articles_set.find_all("a")
		pe_links = pe_articles_set.find_all("a")
		total_article_elements = news_links + pe_links
		article_html_urls = [elem['href'] for elem in total_article_elements]
		article_html_tups = [(requests.get(url).text,url)  for url in article_html_urls]

		print("Caching the new data now...\n")
		CACHE_DICTION[unique_ident] = article_html_tups
		fp = open(CACHE_FNAME,'w')
		fp.write(json.dumps(CACHE_DICTION))
		fp.close()
	print(article_html_tups) #Added this on the branch
	return article_html_tups

# Grab the data
news_pe_articles_tups = get_articles_umich()
soup_article_objs = [BeautifulSoup(element[0]	,"html.parser") for element in news_pe_articles_tups]
# Now I should have a list of BSoup objects!


# Check out a live version to decide what to do with it may be easiest...

all_titles = []
for art in soup_article_objs:

	titleposs = art.find_all("h1")
	title = None # None if there is no title of the article, and then it could be entered in a db table as NULL if you use the None value
	for item in titleposs:
		if item.text:
			title = item.text.strip().rstrip()
		# Note that UMich has already forbidden some scraping on some of the sites so e.g. Renovated nuclear reactor building opens as world-class labs shows up as Forbidden... perils of getting data from the internet!
	# print(title)
	all_titles.append(title)

# And finally...
tuple_results = zip(all_titles,[elem[1] for elem in news_pe_articles_tups])
print(list(tuple_results))

# Lots of things you could do with this! For instance, put this data in a db table...



# Remember, this might take a while to run the first time, just like Project 2!
# (Also, we don't have friends at UMich ITS like we do at UMSI ITS who can set up special headers for us... so don't run this without caching too frequently or we'll get banned!)
