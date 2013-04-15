import os
import sys
import imp
import xbmc
try:    import cPickle as pickle
except: import pickle

from t0mm0.common.addon import Addon
addon = Addon('plugin.video.waldo', sys.argv)

def import_module(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try: return sys.modules[name]
    except KeyError:
        pass

    # If any of the following calls raises an exception,
    # there's a problem we can't handle -- let the caller handle it.
    addon.log_debug('Finding module %s in %s' %(name, fromlist))
    fp, pathname, description = imp.find_module(name,fromlist)

    try: return imp.load_module(name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp: fp.close()

def get_index_name(index):
    addon.log( 'Getting index name of %s' %index)
    return index.__name__.rsplit('.',1)[-1]

def has_requirements(list):
    for addon in list:
        condition = 'System.HasAddon(%s)' %addon
        if not xbmc.getCondVisibility(condition):
            return False
    return True

def _update_settings_xml(list):
    '''
    This function writes a new ``resources/settings.xml`` file which contains
    all settings for this addon and its plugins.
    '''
    settings_file = os.path.join(addon.get_path(), 'resources', 'settings.xml')
    try:
        try:
            os.makedirs(os.path.dirname(settings_file))
        except OSError:
            pass

        f = open(settings_file, 'w')
        try:
            f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write('<settings>\n')    
            for mod in list:
                settings_xml = mod.get_settings_xml()
                if settings_xml:
                    f.write('<category label="%s">\n' % mod.display_name)
                    f.write(settings_xml)
                    f.write('</category>\n')
            f.write('</settings>')
        finally:
            f.close
    except IOError:
        addon.log_error('Error writing ' + common.settings_file)