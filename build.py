from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
use_plugin("python.core")
use_plugin("python.distutils")
use_plugin('copy_resources')
use_plugin('filter_resources')

authors = [Author('Marco Hoyer', 'marco_hoyer@gmx.de')]
description = """checl_http_statusfile: a nagios/icinga check plugin checking an applications statuspage.

for more documentation, visit https://github.com/marco-hoyer/check_http_statuspage
"""

name = 'check_http_statuspage'
summary = 'check_http_statuspage application status page check plugin'
url = 'https://github.com/marco-hoyer/check_http_statuspage'
version = '1.0'

default_task = ['publish']


@init
def initialize(project):
    project.depends_on("argparse")
    project.depends_on("requests")

    project.install_file('/usr/lib64/icinga/plugins', 'check_http_statuspage.py')
    project.install_file('/etc/icinga/conf.d/commands', 'check_http_statuspage.cfg')

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.set_property('install_dependencies_upgrade', True)


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')
