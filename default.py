import sys
sys.modules['xbmcplugin'] = __import__('magic_xbmcplugin')
import os
import imp
import json
import urllib
import xbmc
import urlparse
import xbmcgui
import xbmcplugin

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers
from metahandler import metacontainers

from utils import *

addon = Addon('plugin.video.waldo', sys.argv)
INDEXES_PATH   = os.path.join(addon.get_path(),'indexes')
PROVIDERS_PATH = os.path.join(addon.get_path(),'providers')

def listIndexes():
    import indexes
    for index in indexes.index_list:
        title = index.display_name
        args = {'waldo_mode':'ListIndexBrowsingOptions'}
        args['waldo_mod'] = get_index_name(index)
        args['waldo_path'] = os.path.dirname(index.__file__)
        addon.add_directory(args,   {'title':  title})
    addon.end_of_directory()

def ListIndexBrowsingOptions(index, ind_path):
    index = import_module(index, fromlist=[INDEXES_PATH, ind_path])
    options = index.get_browsing_options()
    for option in options:
        waldo_path, waldo_file = os.path.split(index.__file__)
        queries = {'waldo_mode':'ActivateCallback'}
        queries['waldo_mod'] = waldo_file.rsplit('.',1)[0]
        queries['waldo_path'] = waldo_path
        queries['function'] = option['function']
        queries['kwargs'] = option['kwargs']
        addon.add_directory(queries, {'title':option['name']})
    addon.end_of_directory()

def ActivateCallback(func, kwargs, mod, mod_path):
    mod = import_module(mod, fromlist=[INDEXES_PATH, mod_path])
    callback = getattr(mod, func)
    kwargs = json.loads(kwargs)
    if kwargs: 
        print type(kwargs)
        callback(**kwargs)
    else: callback(addon.queries)

def GetAllResults(vid_type,title,year,imdb,tvdb,season,episode):
    import providers
    for provider in providers.provider_list:
        results = provider.get_results(vid_type,title,year,imdb,tvdb,season,episode)
        for result in results:
            label = '[%s] %s' %(result['tag'], result['info_labels']['title'])
            listitem = xbmcgui.ListItem(label, iconImage='', 
                    thumbnailImage='')
            listitem.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), result['li_url'] , listitem,
                                        isFolder=False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

waldo_mode     = addon.queries.get('waldo_mode',    '')
waldo_mod    = addon.queries.get('waldo_mod',   '')
waldo_path    = addon.queries.get('waldo_path',   '')
name     = addon.queries.get('name',    '')
vid_type     = addon.queries.get('vid_type',    '')
title    = addon.queries.get('title',   '')
year     = addon.queries.get('year',    '')
imdb     = addon.queries.get('imdb',    '')
tvdb     = addon.queries.get('tvdb',    '')
season   = addon.queries.get('season',  '')
episode  = addon.queries.get('episode', '')
function = addon.queries.get('function', 'callback')
kwargs   = addon.queries.get('kwargs',  '{}')
receiver = addon.queries.get('receiver','')

addon.log(addon.queries)
if not 'waldo_mode' in addon.queries:
    listIndexes()
elif waldo_mode=='ListIndexBrowsingOptions':
    ListIndexBrowsingOptions(waldo_mod, waldo_path)
elif waldo_mode=='GetAllResults':
    GetAllResults(vid_type,title,year,imdb,tvdb,season,episode)
elif waldo_mode=='ActivateCallback':
    ActivateCallback(function,kwargs, waldo_mod, waldo_path)
elif waldo_mode=='CallModule':
    receiver = import_module(receiver, fromlist=[INDEXES_PATH,PROVIDERS_PATH, waldo_path])
    receiver.callback(addon.queries)