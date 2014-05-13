# -*- coding: utf-8 -*-


import pkg_resources
import unittest


foo_src = 'render_filename=mrbobby.tests.fake_plugins:FooRenderFilename'
bar_src = 'render_filename=mrbobby.tests.fake_plugins:BarRenderFilename'
bad_src = 'render_filename=mrbobby.tests.fake_plugins:BadRenderFilename'

foo_ep = pkg_resources.EntryPoint.parse(foo_src)
bar_ep = pkg_resources.EntryPoint.parse(bar_src)
bad_ep = pkg_resources.EntryPoint.parse(bad_src)

#unordered_pkg_mock_entries = [bad_ep, bar_ep, foo_ep]
will_continue_mock_ep = [foo_ep]
will_not_continue_mock_ep = [bar_ep]
bad_mock_ep = [bad_ep]


class load_pluginsTest(unittest.TestCase):

    def test_load_plugin_max_order_is_loaded(self):
        import mrbobby.plugins
        ep = mrbobby.plugins.load_plugin('mr.bobby.render_filename', 30)
        self.assertEqual(ep[-1].order, 30)

    def test_error_load_plugin_bad_target(self):
        import mrbobby.plugins
        self.assertRaises(AttributeError, mrbobby.plugins.load_plugin,
                          'mrbobby.render_filename', 19)

    def test_0_taregt_unload_plugins(self):
        import mrbobby.plugins
        ep = mrbobby.plugins.load_plugin('mr.bobby.render_filename', 0)
        self.assertEqual(ep, None)

# vim:set et sts=4 ts=4 tw=80:
