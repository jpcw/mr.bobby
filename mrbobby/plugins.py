# -*- coding: utf-8 -*-

"""Plugins loader.

    You can register your own plugins with entry_points.

    Code a class in your egg and register it within your setup.py file

    .. code-block:: python

        entry_points='''
        # -*- Entry points: -*-
        [mr.bobby.plugins]
        render_filename=bobbyplugins.pkg.module:FooRenderFilename
        ''',

   If there are multiples plugins with same name, you could push yours with
   different **order** attributes.

   If you don't specify an order target `-r, --rdr-fname-plugin-target` the
   plugin with max **order** attribute is prefered,
   otherwise alphabetic sort on namespace returns the last entry.

   If you specify a bad plugin target an error is raised ::

    AttributeError: No plugin target 15 ! Registered are [10, 20]


   .. note:: Please notice that just mrbobby.rendering.render_filename is
    actually plugguable, but code infra is here.

"""

__docformat__ = 'restructuredtext en'

import operator
import pkg_resources

PLUGINS = {}


def load_plugin(plugin, target=None):
    """Load and sort possibles plugins from pkg."""

    if target == 0:
        # unload entry_points
        return
    else:
        entries = [entry for entry in
                   pkg_resources.iter_entry_points(group=plugin)]
        plugins = [(ep, '%d-%s-%s' % (getattr(ep.load(False), 'order', 10),
                                      ep.module_name, ep.name))
                   for ep in entries]
        ordered_plugins = sorted(plugins, key=operator.itemgetter(1))
        if target is not None:
            targets = [ep for ep in ordered_plugins
                       if ep[1].split('-')[0] == str(target)]
            if targets:
                return [targets[-1][0].load(False)]
            else:
                registered = [int(ep[1].split('-')[0])
                              for ep in ordered_plugins]
                raise AttributeError(
                    'No plugin target %d ! Registered are %s' % (target,
                                                                 registered))

        return [ep[0].load(False) for ep in ordered_plugins]

# vim:set et sts=4 ts=4 tw=80:
