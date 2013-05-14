import os
import inspect
import xbmcplugin as mundane_xbmcplugin

from urlparse import urlparse

SORT_METHOD_NONE = 0
SORT_METHOD_LABEL = 1
SORT_METHOD_LABEL_IGNORE_THE = 2
SORT_METHOD_DATE = 3
SORT_METHOD_SIZE = 4
SORT_METHOD_FILE = 5
SORT_METHOD_DRIVE_TYPE = 6
SORT_METHOD_TRACKNUM = 7
SORT_METHOD_DURATION = 8
SORT_METHOD_TITLE = 9
SORT_METHOD_TITLE_IGNORE_THE = 10
SORT_METHOD_ARTIST = 11
SORT_METHOD_ARTIST_IGNORE_THE = 12
SORT_METHOD_ALBUM = 13
SORT_METHOD_ALBUM_IGNORE_THE = 14
SORT_METHOD_GENRE = 15
SORT_METHOD_VIDEO_YEAR =16
SORT_METHOD_VIDEO_RATING = 17

SORT_METHOD_PROGRAM_COUNT = 20
SORT_METHOD_PLAYLIST_ORDER = 21
SORT_METHOD_EPISODE = 22
SORT_METHOD_VIDEO_TITLE = 23

SORT_METHOD_PRODUCTIONCODE = 26
SORT_METHOD_SONG_RATING = 27
SORT_METHOD_MPAA_RATING = 28
SORT_METHOD_VIDEO_RUNTIME = 29
SORT_METHOD_STUDIO = 30
SORT_METHOD_STUDIO_IGNORE_THE = 31

SORT_METHOD_LISTENERS = 36
SORT_METHOD_UNSORTED = 37

SORT_METHOD_BITRATE = 39

#noinspection PyUnusedLocal
def addDirectoryItem(*args, **kwargs):
    """Callback function to pass directory contents back to XBMC.

    Returns a bool for successful completion.

    handle: integer - handle the plugin was started with.
    url: string - url of the entry. would be plugin:// for another virtual directory.
    listitem: ListItem - item to add.
    isFolder: bool - True=folder / False=not a folder.
    totalItems: integer - total number of items that will be passed. (used for progressbar)

    Example:
        if not xbmcplugin.addDirectoryItem(int(sys.argv[1]), 'F:\\Trailers\\300.mov', listitem, totalItems=50):
            break
    """
    caller_path = inspect.stack()[2][1]
    if caller_path.endswith('t0mm0\\common\\addon.py'):
        caller_path = inspect.stack()[3][1]
    caller_path, caller_name = os.path.split(caller_path)
    caller = caller_name.rsplit('.')[0]
    
    parsed = urlparse(args[1])
    if parsed.query:
        if not 'waldo_mod=' in parsed.query:
            args = list(args)
            args[1] = '%s&waldo_mod=%s&waldo_path=%s' %(args[1], caller, caller_path)
        if not 'waldo_mode=' in parsed.query:
            args[1] = '%s&waldo_mode=%s' %(args[1], 'ActivateCallback')
    return mundane_xbmcplugin.addDirectoryItem(*args, **kwargs)

#noinspection PyUnusedLocal
def addDirectoryItems(*args, **kwargs):
    """Callback function to pass directory contents back to XBMC as a list.

    Returns a bool for successful completion.

    handle: integer - handle the plugin was started with.
    items: List - list of (url, listitem[, isFolder]) as a tuple to add.
    totalItems: integer - total number of items that will be passed. (used for progressbar)

    Note:
        Large lists benefit over using the standard addDirectoryItem().
        You may call this more than once to add items in chunks.

    Example:
        if not xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, False,)]:
            raise
    """
    return mundane_xbmcplugin.addDirectoryItems(*args, **kwargs)

#noinspection PyUnusedLocal
def endOfDirectory(*args, **kwargs):
    """Callback function to tell XBMC that the end of the directory listing in a virtualPythonFolder module is reached.

    handle: integer - handle the plugin was started with.
    succeeded: bool - True=script completed successfully/False=Script did not.
    updateListing: bool - True=this folder should update the current listing/False=Folder is a subfolder.
    cacheToDisc: bool - True=Folder will cache if extended time/False=this folder will never cache to disc.

    Example:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    """
    return mundane_xbmcplugin.endOfDirectory(*args, **kwargs)

#noinspection PyUnusedLocal
def setResolvedUrl(*args, **kwargs):
    """Callback function to tell XBMC that the file plugin has been resolved to a url

    handle: integer - handle the plugin was started with.
    succeeded: bool - True=script completed successfully/False=Script did not.
    listitem: ListItem - item the file plugin resolved to for playback.

    Example:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    """
    return mundane_xbmcplugin.setResolvedUrl(*args, **kwargs)

#noinspection PyUnusedLocal
def addSortMethod(*args, **kwargs):
    """Adds a sorting method for the media list.

    handle: integer - handle the plugin was started with.
    sortMethod: integer - number for sortmethod see FileItem.h.
    label2Mask: string - the label mask to use for the second label.  Defaults to '%D'
        applies to: SORT_METHOD_NONE, SORT_METHOD_UNSORTED, SORT_METHOD_VIDEO_TITLE,
        SORT_METHOD_TRACKNUM, SORT_METHOD_FILE, SORT_METHOD_TITLE
        SORT_METHOD_TITLE_IGNORE_THE, SORT_METHOD_LABEL
        SORT_METHOD_LABEL_IGNORE_THE

    Example:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    """
    return mundane_xbmcplugin.addSortMethod(*args, **kwargs)

#noinspection PyUnusedLocal
def getSetting(*args, **kwargs):
    """Returns the value of a setting as a string.

    handle: integer - handle the plugin was started with.
    id: string - id of the setting that the module needs to access.

    Example:
        apikey = xbmcplugin.getSetting(int(sys.argv[1]), 'apikey')
    """
    return mundane_xbmcplugin.getSetting(*args, **kwargs)

#noinspection PyUnusedLocal
def setSetting(*args, **kwargs):
    """Sets a plugin setting for the current running plugin.

    handle: integer - handle the plugin was started with.
    id: string - id of the setting that the module needs to access.
    value: string or unicode - value of the setting.

    Example:
        xbmcplugin.setSetting(int(sys.argv[1]), id='username', value='teamxbmc')
    """
    return mundane_xbmcplugin.setSetting(*args, **kwargs)

#noinspection PyUnusedLocal
def setContent(*args, **kwargs):
    """Sets the plugins content.

    handle: integer - handle the plugin was started with.
    content: string - content type (eg. movies).

    Note:
        Possible values for content: files, songs, artists, albums, movies, tvshows, episodes, musicvideos

    Example:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    """
    return mundane_xbmcplugin.setContent(*args, **kwargs)

#noinspection PyUnusedLocal
def setPluginCategory(*args, **kwargs):
    """Sets the plugins name for skins to display.

    handle: integer - handle the plugin was started with.
    category: string or unicode - plugins sub category.

    Example:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Comedy')
    """
    return mundane_xbmcplugin.setPluginCategory(*args, **kwargs)

#noinspection PyUnusedLocal
def setPluginFanart( *args, **kwargs):
    """Sets the plugins fanart and color for skins to display.

    handle: integer - handle the plugin was started with.\n"
    image: string - path to fanart image.
    color1: hexstring - color1. (e.g. '0xFFFFFFFF')
    color2: hexstring - color2. (e.g. '0xFFFF3300')
    color3: hexstring - color3. (e.g. '0xFF000000')

    Example:
        xbmcplugin.setPluginFanart(int(sys.argv[1]), 'special://home/addons/plugins/video/Apple movie trailers II/fanart.png', color2='0xFFFF3300')
    """
    return mundane_xbmcplugin.setPluginFanart( *args, **kwargs)

#noinspection PyUnusedLocal
def setProperty( *args, **kwargs):
    """Sets a container property for this plugin.

    handle: integer - handle the plugin was started with.
    key: string - property name.
    value: string or unicode - value of property.

    Note:
        Key is NOT case sensitive.

    Example:
        xbmcplugin.setProperty(int(sys.argv[1]), 'Emulator', 'M.A.M.E.')
    """
    return mundane_xbmcplugin.setProperty(*args, **kwargs)