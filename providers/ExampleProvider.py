display_name = 'Example Provider'
#MUST be implemented. String that will be used to represent this provider to the user

required_addons = []
#MUST be implemented. A list of strings indicating which addons are required to
#be installed for this provider to be used.
#For example: required_addons = ['script.module.beautifulsoup', 'plugin.video.youtube']
#Currently, xbmc does not provide a way to require a specific version of an addon

tag = 'ExP'
#MUST be implemented. Unique 3 or 4 character string that will be used to
#denote content from this provider

def get_settings_xml():
    '''
    Must be defined. This method should return XML which describes any Waldo
    specific settings you would like for your plugin. You should make sure that
    the ``id`` starts with your tag followed by an underscore.
    
    For example:
        xml = '<setting id="ExI_priority" '
        xml += 'type="number" label="Priority" default="100"/>\\n'
        return xml 

    The settings category will be your plugin's :attr:`display_name`.

    Returns:
        A string containing XML which would be valid in 
        ``resources/settings.xml`` or boolean False if none are required
    '''
    return False

def get_results(vid_type,title,year,imdb,tvdb,season,episode):#MUST be implemented
	'''
	Should accept ALL of the following parameters:
	vid_type: A string, either 'movie', 'tvshow', 'season', or 'episode'
	title: A string indicating the movie or tvshow title to find sources for
	year: A string indicating the release date of the desired movie, or premiere
		date of the desired tv show.
	imdb: A string or int of the imdb id of the movie or tvshow to find sources for
	tvdb: A string or int of the tvdb id of the movie or tvshow to find sources for
	season: A string or int indicating the season for which to return results.
		If season is supplied, but not episode, all results for that season
		should be returned
	episode: A string or int indicating the episode for which to return results
	
	If the source cannot filter results based one of these parameters, that
	parameter should be silently ignored.
	'''

	if   vid_type=='movie'  : return _get_movies(title,year,imdb)
	elif vid_type=='tvshow' : return _get_tvshows(title,year,imdb,tvdb)
	elif vid_type=='season' : return _get_season(title,year,imdb,tvdb,season)
	elif vid_type=='episode': return _get_episodes(title,year,imdb,tvsb,season,episode)
	#These are just example function names, the function name doesn't matter,
	#as long as it returns the expected result, which is described in these
	#example functions

def callback(params):
	'''
	MUST be implemented. This method allows you to call functions from your listitems.
	When Waldo is called with mode=CallModule, the callback() function of the module
	who's filename matches the receiver parameter will be called and passed all a dict
	of all the parameters.
	For example, to call this example function, you would call:
		plugin://plugin.video.waldo/?mode=CallModule&receiver=ExampleIndex
	'''
	addon.log('%s was called with the following parameters: %s' %(params.get('receiver',''), params))

def _get_movies(title,year,imdb):
	results = []
	result_1 = {}#Each result must be a dict with ALL of the following fields returned.
				 #If this source does not provide that particular piece of information,
				 #return '' (the empty string) in that field
	result_1['tag'] = tag
	result_1['provider_name'] = display_name
	result_1['li_url'] = 'plugin://plugin.video.waldo'

	result_1['info_labels'] = {'title':'Movie Result 1'}
    #A dict of infolabels to be set for this item

	results.append(result_1)
	return results

def result_1_function(res_num,url):
	print 'Result %s from 1Channel function was called. It\'s url is %s'%(res_num,url)

def result_2_function(res_num,url):
	print 'Result 2 from 1Channel function was called'

def result_3_function(res_num,url):
	print 'Result 3 from 1Channel function was called'