import os
import posixpath

from fabric.api import run
from fabric.contrib import files

from .containers import conf
from .task import Task


__all__ = [
    'push_config',
    'build',
    'init',
    'activate'
]


class PushConfig(Task):
    @conf
    def from_file(self):
        return os.path.join(
            self.conf.project_dir, self.conf.remote_anjsettings_lfile)

    @conf
    def to_file(self):
        return posixpath.join(
            self.conf.project_path, self.conf.local_anjsettings_file)

    def do(self):
        files.upload_template(
            self.conf.from_file,
            self.conf.to_file,
            context=self.conf,
            use_jinja=True)

push_config = PushConfig()


class Build(Task):
    @conf
    def options(self):
        return ''

    def do(self):
        run('cd %(project_path)s/ui; ./scripts/production.sh' % self.conf)

build = Build()


class Init(Task):
    @conf
    def options(self):
        return ''

    def do(self):
        run('cd %(project_path)s/ui; ./scripts/init.sh' % self.conf)
        run('cp -r %(project_path)s/ui/node_modules %(var_path)s/node_modules' % self.conf)
        run('rm --force %(project_path)s/ui/node_modules' % self.conf)

init = Init()

class Activate(Task):
    @conf
    def options(self):
        return ''

    def do(self):
        run('ln '
            '--symbolic '
            '--force '
            '--no-target-directory '
            '%(var_path)s/node_modules %(project_path)s/ui/node_modules' % self.conf)

activate = Activate()
