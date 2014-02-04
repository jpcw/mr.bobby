# -*- coding: utf-8 -*-


import pkg_resources
import unittest


foo_src = 'render_filename=mrbobby.tests.fake_plugins:FooRenderFilename'
bar_src = 'render_filename=mrbobby.tests.fake_plugins:BarRenderFilename'
bad_src = 'render_filename=mrbobby.tests.fake_plugins:BadRenderFilename'

foo_ep = pkg_resources.EntryPoint.parse(foo_src)
bar_ep = pkg_resources.EntryPoint.parse(bar_src)
bad_ep = pkg_resources.EntryPoint.parse(bad_src)

unordered_pkg_mock_entries = [bad_ep, bar_ep, foo_ep]
will_continue_mock_ep = [foo_ep]
bad_mock_ep = [bad_ep]


class load_pluginsTest(unittest.TestCase):

    def test_load_plugin_max_order_is_loaded(self):
        import mrbobby.plugins
        ep = mrbobby.plugins.load_plugin('render_filename',
                                         unordered_pkg_mock_entries)
        self.assertEqual(ep.order, 20)

    def test_load_plugin_target_is_loaded(self):
        import mrbobby.plugins
        ep = mrbobby.plugins.load_plugin('render_filename',
                                         unordered_pkg_mock_entries,
                                         target=15)

        self.assertEqual(ep.order, 15)

    def test_error_load_plugin_bad_target(self):
        import mrbobby.plugins
        self.assertRaises(AttributeError, mrbobby.plugins.load_plugin,
                          'render_filename', unordered_pkg_mock_entries,
                          target=19)

# vim:set et sts=4 ts=4 tw=80:
