import unittest

import numpy
import sys
import os
import unittest
import warnings

# Add parent directory to path to make test aware of other modules
pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(pardir)

# FIXME (Ole): Must use fully qualified path for these
from impact_functions.core import FunctionProvider
from impact_functions.core import get_plugins

from core import requirements_collect
from core import requirement_check
from core import compatible_layers

from storage.core import read_layer
from storage.utilities_test import TESTDATA

DEFAULT_PLUGINS = ('Earthquake Fatality Function',)


# FIXME (Ole): Change H, E to layers.
class BasicFunction(FunctionProvider):
    """Risk plugin for testing

    :author Allen
    :rating 1
    :param requires category=="hazard"
    """

    @staticmethod
    def run(H, E,
            a=0.97429, b=11.037):

        return None


class Test_plugins(unittest.TestCase):
    """Tests of Risiko calculations
    """

    def test_get_plugins(self):
        """It is possible to retrieve the list of functions
        """
        plugin_list = plugins.get_plugins()
        msg = ('No plugins were found, not even the built-in ones')
        assert len(plugin_list) > 0, msg

    def test_single_get_plugins(self):
        """Named plugin can be retrieved
        """
        plugin_name = DEFAULT_PLUGINS[0]
        plugin_list = get_plugins(plugin_name)
        msg = ('No plugins were found matching %s' % plugin_name)
        assert len(plugin_list) > 0, msg

    def test_get_plugins(self):
        """Plugins can be collected
        """

        plugin_list = get_plugins()
        assert(len(plugin_list) > 0)

        # Check that every plugin has a requires line
        for plugin in plugin_list.values():
            requirements = requirements_collect(plugin)
            msg = 'There were no requirements in plugin %s' % plugin
            assert(len(requirements) > 0), msg

            for req_str in requirements:
                msg = 'All plugins should return True or False'
                assert(requirement_check({'category': 'hazard',
                                          'subcategory': 'earthquake',
                                          'layerType': 'raster'},
                                         req_str) in [True, False]), msg

    def test_requirements_check(self):
        """Plugins are correctly filtered based on requirements"""

        plugin_list = get_plugins('BasicFunction')
        assert(len(plugin_list) == 1)

        requirements = requirements_collect(plugin_list[0].values()[0])
        msg = 'Requirements are %s' % requirements
        assert(len(requirements) == 1), msg
        for req_str in requirements:
            msg = 'Should eval to True'
            assert(requirement_check({'category': 'hazard'},
                                     req_str) is True), msg
            msg = 'Should eval to False'
            assert(requirement_check({'broke': 'broke'},
                                     req_str) is False), msg

        try:
            plugin_list = get_plugins('NotRegistered')
        except AssertionError:
            pass
        else:
            msg = 'Search should fail'
            raise Exception(msg)

    def test_plugin_compatibility(self):
        """Default plugins perform as expected
        """

        # Get list of plugins
        plugin_list = get_plugins()
        assert len(plugin_list) > 0

        # Characterisation test to preserve the behaviour of
        # get_layer_descriptors. FIXME: I think we should change this to be
        # a dictionary of metadata entries (ticket #126).
        reference = [['lembang_schools',
                      {'layertype': 'vector',
                       'category': 'exposure',
                       'subcategory': 'building',
                       'title': 'lembang_schools'}],
                     ['shakemap_padang_20090930',
                      {'layertype': 'raster',
                       'category': 'hazard',
                       'subcategory': 'earthquake',
                       'title': 'shakemap_padang_20090930'}]]

        # Check plugins are returned
        metadata = reference
        annotated_plugins = [{'name': name,
                              'doc': f.__doc__,
                              'layers': compatible_layers(f, metadata)}
                             for name, f in plugin_list.items()]

        msg = 'No compatible layers returned'
        assert len(annotated_plugins) > 0, msg


if __name__ == '__main__':
    suite = unittest.makeSuite(Test_plugins, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
