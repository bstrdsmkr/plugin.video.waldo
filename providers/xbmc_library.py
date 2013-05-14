import json
import xbmc

display_name = 'Xbmc Library'
#MUST be implemented. String that will be used to represent this provider to the user

required_addons = []
#MUST be implemented. A list of strings indicating which addons are required to
#be installed for this provider to be used.
#For example: required_addons = ['script.module.beautifulsoup', 'plugin.video.youtube']
#Currently, xbmc does not provide a way to require a specific version of an addon

tag = 'Xbmc'
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

def get_results(vid_type, title, year, imdb, tvdb, season, episode):#MUST be implemented
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
    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "streamdetails", "genre", "studio", "year", "tagline", "plot", "plotoutline", "runtime", "fanart", "thumbnail", "file", "trailer", "playcount", "rating", "mpaa", "director", "writer"], "sort": { "method": "label" }, "filter": { "or":[{"field":"title","operator":"contains","value":"%s"},{"field":"title","operator":"contains","value":"%s"}] }}, "id": 1}' % (title, title))
    json_response = json.loads(json_query)
    if (json_response['result'] != None) and (json_response['result'].has_key('movies')):
        for item in json_response['result']['movies']:
            movie = item['title']
            director = " / ".join(item['director'])
            writer = " / ".join(item['writer'])
            fanart = item['fanart']
            path = item['file']
            genre = " / ".join(item['genre'])
            mpaa = item['mpaa']
            playcount = str(item['playcount'])
            plot = item['plot']
            outline = item['plotoutline']
            rating = str(round(float(item['rating']),1))
            starrating = 'rating%.1d.png' % round(float(rating)/2)
            runtime = str(item['runtime'] / 60)
            studio = " / ".join(item['studio'])
            tagline = item['tagline']
            thumb = item['thumbnail']
            trailer = item['trailer']
            year = str(item['year'])
            if item['streamdetails']['audio'] != []:
                audiochannels = str(item['streamdetails']['audio'][0]['channels'])
                audiocodec = str(item['streamdetails']['audio'][0]['codec'])
            else:
                audiochannels = ''
                audiocodec = ''
            if item['streamdetails']['video'] != []:
                videocodec = str(item['streamdetails']['video'][0]['codec'])
                videoaspect = float(item['streamdetails']['video'][0]['aspect'])
                if videoaspect <= 1.4859:
                    videoaspect = '1.33'
                elif videoaspect <= 1.7190:
                    videoaspect = '1.66'
                elif videoaspect <= 1.8147:
                    videoaspect = '1.78'
                elif videoaspect <= 2.0174:
                    videoaspect = '1.85'
                elif videoaspect <= 2.2738:
                    videoaspect = '2.20'
                else:
                    videoaspect = '2.35'
                videowidth = item['streamdetails']['video'][0]['width']
                videoheight = item['streamdetails']['video'][0]['height']
                if videowidth <= 720 and videoheight <= 480:
                    videoresolution = '480'
                elif videowidth <= 768 and videoheight <= 576:
                    videoresolution = '576'
                elif videowidth <= 960 and videoheight <= 544:
                    videoresolution = '540'
                elif videowidth <= 1280 and videoheight <= 720:
                    videoresolution = '720'
                else:
                    videoresolution = '1080'
            else:
                videocodec = ''
                videoaspect = ''
                videoresolution = ''

            result = {'tag':tag, 'provider_name':display_name, 'li_url':path}
            result['info_labels'] = {'icon': thumb, 'title': movie}
            result['info_labels']['fanart'] = fanart
            result['info_labels']['genre'] = genre
            result['info_labels']['plot'] = plot
            result['info_labels']['plotoutline'] = outline
            result['info_labels']['duration'] = runtime
            result['info_labels']['studio'] = studio
            result['info_labels']['tagline'] = tagline
            result['info_labels']['year'] = year
            result['info_labels']['trailer'] = trailer
            result['info_labels']['playcount'] = playcount
            result['info_labels']['rating'] = rating
            result['info_labels']['starrating'] = starrating
            result['info_labels']['mpaa'] = mpaa
            result['info_labels']['writer'] = writer
            result['info_labels']['director'] = director
            result['info_labels']['videoresolution'] = videoresolution
            result['info_labels']['videocodec'] = videocodec
            result['info_labels']['videoaspect'] = videoaspect
            result['info_labels']['audiocodec'] = audiocodec
            result['info_labels']['audiochannels'] = audiochannels
            yield result

def result_1_function(res_num,url):
	print 'Result %s from 1Channel function was called. It\'s url is %s'%(res_num,url)

def result_2_function(res_num,url):
	print 'Result 2 from 1Channel function was called'

def result_3_function(res_num,url):
	print 'Result 3 from 1Channel function was called'