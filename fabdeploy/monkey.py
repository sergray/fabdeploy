from fabric import operations
from fabric.contrib import files
from fabric.api import sudo, env

from .utils import sudo_user


__all__ = ['patch_all']


_run_command = operations._run_command
put = operations.put


def _patched_run_command(
    command,
    shell=True,
    pty=True,
    combine_stderr=True,
    sudo=False,
    user=None,
    quiet=False, warn_only=False, stdout=None, stderr=None, group=None):
    if sudo:
        with sudo_user():
            return _run_command(command, shell=shell, pty=pty,
                combine_stderr=combine_stderr, sudo=sudo, user=user, group=group,
                quiet=quiet, warn_only=warn_only, stdout=stdout, stderr=stderr)
    else:
        return _run_command(command, shell=shell, pty=pty,
            combine_stderr=combine_stderr, sudo=sudo, user=env.conf.user, group=group,
            quiet=quiet, warn_only=warn_only, stdout=stdout, stderr=stderr)


def patched_put(
    local_path=None,
    remote_path=None,
    use_sudo=False,
    mirror_local_mode=False,
    mode=None):
    if use_sudo:
        with sudo_user():
            return put(local_path=local_path, remote_path=remote_path,
                use_sudo=use_sudo, mirror_local_mode=mirror_local_mode,
                mode=mode)
    else:
        return put(local_path=local_path, remote_path=remote_path,
            use_sudo=use_sudo, mirror_local_mode=mirror_local_mode, mode=mode)


def patch_all():
    operations._run_command = _patched_run_command
    operations.put = patched_put
    files.put = patched_put
