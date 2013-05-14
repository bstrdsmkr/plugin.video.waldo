#Providers
import os
import sys

from utils import *
from t0mm0.common.addon import Addon
addon = Addon('plugin.video.waldo', sys.argv)
provider_list = []
for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	mod = __import__(module[:-3], locals(), globals())
	if has_requirements(mod.required_addons):
		addon.log_debug('Waldo: Importing %s as provider' %module)
		provider_list.append(mod)
	else:
		addon.log_debug('Waldo: Requirements not met for %s' %mod.display_name)
		del mod
del module

addons_dir = xbmc.translatePath(os.path.join('special://home','addons'))
addon.log_debug('Addons directory: %s' %addons_dir)
for node in os.listdir(addons_dir):
    node = os.path.join(addons_dir, node)
    if os.path.isdir(node):
        provider_dir = os.path.join(node, 'waldo', 'providers')
        addon.log_debug('Looking for %s' %provider_dir)
        if os.path.exists(provider_dir):
            for module in os.listdir(provider_dir):
                if (module == '__init__.py') or (module[-3:] != '.py'):
                    continue
                mod = import_module(module[:-3], fromlist=[provider_dir,])
                if has_requirements(mod.required_addons):
                    addon.log_debug('Waldo: importing %s as index' %module)
                    provider_list.append(mod)
                else:
                    addon.log_debug('Waldo: Requirements not met for %s' %mod.display_name)
                    del mod
            del module
update_settings_xml(provider_list)