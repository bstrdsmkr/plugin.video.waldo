import sys

from t0mm0.common.addon import Addon
addon = Addon('plugin.video.waldo', sys.argv)

display_name = 'Example Index'
#Label that will be displayed to the user representing this index

tag = 'ExI'
#MUST be implemented. Unique 3 or 4 character string that will be used to
#identify this index

required_addons = []
#MUST be implemented. A list of strings indicating which addons are required to
#be installed for this index to be used.
#For example: required_addons = ['script.module.beautifulsoup', 'plugin.video.youtube']
#Currently, xbmc does not provide a way to require a specific version of an addon

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

def get_browsing_options():#MUST be defined
	'''
	Returns a list of dicts. Each dict represents a different method of browsing
	this index. The following keys MUST be provided:
	'name': Label to display to the user to represent this browsing method
	'function': A function (defined in this index) which will be executed when
		the user selections this browsing method. This function should describe
		and add the list items to the directory, and assume flow control from
		this point on.
	Once the user indicates the content they would like to search the providers
	for (usually via selecting a list item), plugin.video.waldo should be called
	with the following parameters (again usually via listitem):
		mode = 'GetAllResults'
		type = either 'movie', 'tvshow', 'season', or 'episode'
		title = The title string to look for
		year = The release year of the desired movie, or premiere date of the
			desired tv show.
		imdb = The imdb id of the movie or tvshow to find sources for
		tvdb = The tvdb id of the movie or tvshow to find sources for
		season = The season number for which to return results.
			If season is supplied, but not episode, all results for that season
			should be returned
		episode: The episode number for which to return results
	'''
	option_1 = {}
	option_1['name'] = 'Browsing Option 1'
	option_1['function'] = browsing_option_1
	option_1['kwargs'] = {'dummykey':'dummyvalue'}

	option_2 = {}
	option_2['name'] = 'Browsing Option 2'
	option_2['function'] = browsing_option_2
	option_2['kwargs'] = {'dummykey':'dummyvalue'}

	option_3 = {}
	option_3['name'] = 'Browsing Option 3'
	option_3['function'] = browsing_option_3
	option_3['kwargs'] = {'dummykey':'dummyvalue'}
	
	return [option_1,option_2,option_3]

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

def browsing_option_1(dummykey): #This must match the 'function' key of an option from get_browsing_options
	addon.add_directory({'mode':'GetAllResults', 'type':'movie'},   {'title':'Content 1 of Browsing Option 1'})
	addon.add_directory({'mode':'dummy'},   {'title':'Content 2 of Browsing Option 1'})
	addon.add_directory({'mode':'dummy'},   {'title':'Content 3 of Browsing Option 1'})
	addon.end_of_directory()

def browsing_option_2(): #This must match the function key of an option from get_browsing_options
	print 'Browsing Option 2 has been called'

def browsing_option_3(): #This must match the function key of an option from get_browsing_options
	print 'Browsing Option 3 has been called'

