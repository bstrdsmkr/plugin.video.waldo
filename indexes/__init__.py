#Indexes
import os
import sys

from utils import has_requirements, _update_settings_xml
from t0mm0.common.addon import Addon
addon = Addon('plugin.video.waldo', sys.argv)
index_list = []
for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	mod = __import__(module[:-3], locals(), globals())
	if has_requirements(mod.required_addons):
		addon.log_debug('Waldo: importing %s as index' %module)
		index_list.append(mod)
	else:
		addon.log_debug('Waldo: Requirements not met for %s' %mod.display_name)
		del mod
del module

_update_settings_xml(index_list)