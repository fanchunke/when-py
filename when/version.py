"""The `version` module holds the version information for when-py."""
__all__ = 'VERSION', 'version_info'

VERSION = '0.1.0'


def version_info() -> str:
    """Return complete version information for when-py."""
    import platform
    import sys
    from pathlib import Path

    info = {
        'when-py version': VERSION,
        'install path': Path(__file__).resolve().parent,
        'python version': sys.version,
        'platform': platform.platform(),
    }
    return '\n'.join('{:>30} {}'.format(k + ':', str(v).replace('\n', ' ')) for k, v in info.items())
