from os.path import dirname, basename, isfile
import glob
import pbr.version

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

# Setup version
VERSION = pbr.version.VersionInfo('pyansible')
try:
    __version__ = VERSION.version_string()
    __release__ = VERSION.release_string()
except (ValueError, AttributeError):
    __version__ = None
__release__ = None
