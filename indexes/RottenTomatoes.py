import sys
import json
import gzip
import urllib2
import xbmcplugin
from StringIO import StringIO

from t0mm0.common.addon import Addon
addon = Addon('plugin.video.waldo', sys.argv)
api_key = addon.get_setting('Rtn_api_key')

display_name = 'Rotten Tomatoes'
#Label that will be displayed to the user representing this index

tag = 'Rtn'
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
    xml =  '<setting id="Rtn_api_key" '
    xml += 'type="text" label="API Key" default=""/>\\n'
    return xml 

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
    
    if not api_key: return []
    url = 'http://api.rottentomatoes.com/api/public/v1.0/lists.json?apikey=%s'
    url = url % api_key
    page = GetURL(url)
    response = json.loads(page)

    option_1 = {}
    option_1['name'] = 'Movies'
    option_1['function'] = 'movies'
    option_1['kwargs'] = {}

    option_2 = {}
    option_2['name'] = 'DVDs'
    option_2['function'] = 'dvds'
    option_2['kwargs'] = {}
    
    return [option_1,option_2]

def callback(params):
    '''
    MUST be implemented. This method will be called when the user selects a
    listitem you created. It will be passed a dict of parameters you passed to
    the listitem's url.
    For example, the following listitem url:
        plugin://plugin.video.waldo/?mode=main&section=tv&api_key=1234
     Will call this function with:
        {'mode':'main', 'section':'tv', 'api_key':'1234'}
    '''
    addon.log('%s was called with the following parameters: %s' %(__file__, params))
    mode = params.get('mode')
    if mode == 'list_content': list_content(params.get('url'))
    
def movies(params):
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?apikey=%s'}, {'title':'Box Office'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=%s'}, {'title':'In Theaters'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/opening.json?apikey=%s'}, {'title':'Opening'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/upcoming.json?apikey=%s'}, {'title':'Upcoming'})
    addon.end_of_directory()


def dvds(params):
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/top_rentals.json?apikey=%s'}, {'title':'Top Rentals'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/current_releases.json?apikey=%s'}, {'title':'Current Releases'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/new_releases.json?apikey=%s'}, {'title':'New Releases'})
    addon.add_directory({'mode':'list_content', 'url':'http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/upcoming.json?apikey=%s'}, {'title':'Upcoming'})
    addon.end_of_directory()


def list_content(url):
    url = url % api_key
    response = json.loads(GetURL(url))
    
    for movie in response['movies']:
        print movie
        title = '%s (%s)' %(movie['title'], movie['year'])
        li_params = {'waldo_mode':'GetAllResults', 'vid_type':'movie'}
        li_params['title'] = movie['title']
        li_params['year'] = movie['year']
        if 'alternate_ids' in movie:
            li_params['imdb'] = movie['alternate_ids']['imdb']
        else:
            li_params['imdb'] = ''
        
        info_labels = {'title':title, 'year':movie['year']}
        addon.add_directory(li_params, info_labels, img=movie['posters']['detailed'])
    addon.end_of_directory()


def GetURL(url):
    addon.log('Fetching URL: %s' % url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        return f.read()
    return response.read()