from os import path
from shutil import copy2
import codecs
import fnmatch
import os
import re
import six
import stat

from jinja2 import Environment, StrictUndefined
import mrbobby.plugins as plugins

jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
    undefined=StrictUndefined,
)

jinja2_renderer = lambda s, v: jinja2_env.from_string(
    s).render(parse_variables(v))
python_formatting_renderer = lambda s, v: s % v

DEFAULT_IGNORED = ['.mrbobby.ini', '.DS_Store']


def parse_variables(variables):
    d = dict()

    for key, value in variables.items():
        keys = key.split('.')
        new_d = None
        for k in keys[:-1]:
            if new_d is None:
                if k not in d:
                    d[k] = dict()
                new_d = d[k]
            else:
                if k not in new_d:
                    new_d[k] = dict()
                new_d = new_d[k]
        if new_d is None:
            d[keys[-1]] = value
        else:
            new_d[keys[-1]] = value
    return dict(d)


def matches_any(filename, patterns):
    result = any(fnmatch.fnmatch(filename, pat) for pat in patterns)
    return result


def render_structure(fs_source_root, fs_target_root, variables, verbose,
                     renderer, ignored_files):
    """
    Recursively copies the given filesystem path `fs_source_root_` to a
    target directory `fs_target_root`.

    Any files ending in `.bobby` are rendered as templates using the given
    renderer using the variables dictionary, thereby losing the `.bobby`
    suffix.

    strings wrapped in `+` signs in file- or directory names will be replaced
    with values from the variables, i.e. a file named `+name+.py.bobby` given a
    dictionary {'name': 'bar'} would be rendered as `bar.py`.
    """

    ignored_files.extend(DEFAULT_IGNORED)
    if not isinstance(fs_source_root, six.text_type):  # pragma: no cover
        fs_source_root = six.u(fs_source_root)
    for fs_source_dir, local_dirs, local_files in os.walk(fs_source_root):
        fs_target_dir = path.abspath(
            path.join(fs_target_root, path.relpath(fs_source_dir,
                                                   fs_source_root)))
        for local_file in local_files:
            if matches_any(local_file, ignored_files):
                continue
            filename = render_filename(fs_target_dir, variables)
            if filename is not None:
                render_template(
                    path.join(fs_source_dir, local_file),
                    filename,
                    variables,
                    verbose,
                    renderer,
                )
        for local_directory in local_dirs:
            abs_dir = render_filename(
                path.join(fs_target_dir, local_directory), variables)
            if abs_dir is not None:
                if not path.exists(abs_dir):
                    if verbose:
                        print(six.u("mkdir %s") % abs_dir)
                    os.mkdir(abs_dir)


def render_template(fs_source, fs_target_dir, variables, verbose, renderer):
    filename = render_filename(path.split(fs_source)[1], variables)
    if filename is not None:
        if filename.endswith('.bobby'):
            filename = filename.split('.bobby')[0]
            fs_target_path = path.join(fs_target_dir, filename)
            if verbose:
                print(six.u("Rendering %s to %s") %
                      (fs_source, fs_target_path))
            fs_source_mode = stat.S_IMODE(os.stat(fs_source).st_mode)
            with codecs.open(fs_source, 'r', 'utf-8') as f:
                source_output = f.read()
                output = renderer(source_output, variables)
                if source_output.endswith('\n') and not output.endswith('\n'):
                    output += '\n'  # pragma: no cover
            with codecs.open(fs_target_path, 'w', 'utf-8') as fs_target:
                fs_target.write(output)
            os.chmod(fs_target_path, fs_source_mode)
        else:
            fs_target_path = path.join(fs_target_dir, filename)
            if verbose:
                print(six.u("Copying %s to %s") % (fs_source, fs_target_path))
            copy2(fs_source, fs_target_path)
        return path.join(fs_target_dir, filename)


def render_filename(filename, variables):
    """Overridable (via entry_points) rendering.

    Now plugguable, see :ref:`writing your plugin` to
    modify your replacements or other variables substitutions.

    This is a useful option to generate templates or conditionnal rendering.

    """

    rdr_fname_plugins = plugins.PLUGINS.get('mr.bobby.render_filename')
    if rdr_fname_plugins is not None:
        for plugin in rdr_fname_plugins:
            if getattr(plugin, 'get_filename', None) is None:
                raise AttributeError('get_filename method not found in plugin')
            else:
                plug_inst = plugin(filename, variables)
                filename, will_continue = plug_inst.get_filename()
                if filename is None or not will_continue:
#                    break
                    return filename

    variables_regex = re.compile(r"\+[^+%s]+\+" % re.escape(os.sep))

    replaceables = variables_regex.findall(filename)
    for replaceable in replaceables:
        actual_replaceable = replaceable.replace('+', '')
        if actual_replaceable in variables:
            filename = filename.replace(
                replaceable, variables[actual_replaceable])
        else:
            raise KeyError(
                '%s key part of filename %s was not found in variables %s' %
                (actual_replaceable, filename, variables))
    return filename
