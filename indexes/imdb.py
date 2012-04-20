import sys

from t0mm0.common.addon import Addon

addon = Addon('plugin.video.waldo', sys.argv)
display_name = 'Internet Movie Database'
required_addons = []

SEARCH_URL = 'http://m.imdb.com/search/title?'

def get_browsing_options():#MUST be defined
	#by genre
	addon.add_directory({'mode':'ActivateCallback', 'function':_browse_by_genre, 'kwargs':},   {'title':'Content 1 of Browsing Option 1'})
	#by number of votes
	#by A-Z
	#by decade

	return [option_1,option_2,option_3]

def _browse_by_genre():
	pass

def title_search(params, start="1"):
#http://m.imdb.com/search/title?count=250&num_votes=1,100000&production_status=released&sort=year,asc&title_type=feature&view=simple&year=1990,2000
    params["count"] = COUNT
    params["view"] = VIEW
    #params["num_votes"] = NUM_VOTES
    #params["user_rating"] = USER_RATING
    params["start"] = start
    url = SEARCH_URL
    for key in params:
        url += "%s=%s&" % (key, params[key])
    body = get_url(url, cache=CACHE_PATH, cache_time=86400)  
    return body

def browsing_option_1(dummykey): #This must match the function key of an option from get_browsing_options
	addon.add_directory({'mode':'GetAllResults', 'type':'movie'},   {'title':'Content 1 of Browsing Option 1'})
	addon.add_directory({'mode':'dummy'},   {'title':'Content 2 of Browsing Option 1'})
	addon.add_directory({'mode':'dummy'},   {'title':'Content 3 of Browsing Option 1'})
	addon.end_of_directory()

def browsing_option_2(): #This must match the function key of an option from get_browsing_options
	print 'Browsing Option 2 has been called'

def browsing_option_3(): #This must match the function key of an option from get_browsing_options
	print 'Browsing Option 3 has been called'

