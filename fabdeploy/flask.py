import os
import posixpath
from fabric.contrib import files

from .containers import conf
from .task import Task

__all__ = [
    'push_flask_config',
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
