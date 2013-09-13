import os
import posixpath

from fabric.contrib import files
from fabric.api import run

from .containers import conf
from .task import Task
from .utils import inside_django

__all__ = [
    'push_flask_config',
    'manage',
    'migrate'
]


class PushFlaskConfig(Task):
    @conf
    def from_file(self):
        return os.path.join(
            self.conf.django_dir, self.conf.remote_settings_lfile)

    @conf
    def to_file(self):
        return posixpath.join(
            self.conf.django_path, self.conf.local_settings_file)

    def do(self):
        files.upload_template(
            self.conf.from_file,
            self.conf.to_file,
            context=self.conf,
            use_jinja=True)

push_flask_config = PushFlaskConfig()

class Manage(Task):
    @conf
    def options(self):
        return ''

    @inside_django
    def do(self):
        run('python manage.py %(command)s %(options)s' % self.conf)

manage = Manage()

class Migrate(Manage):
    @conf
    def command(self):
        return 'migrate'

migrate = Migrate()
