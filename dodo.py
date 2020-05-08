from pyct import *

############################################################
# TODO: remove if project is updated to use pyctdev
miniconda_url = {
    "Windows": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe",
    "Linux": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
    "Darwin": "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
}
def task_download_miniconda():
    import platform

    try:
        from urllib.request import urlretrieve
    except ImportError:
        from urllib import urlretrieve
    
    url = miniconda_url[platform.system()]
    miniconda_installer = url.split('/')[-1]

    def download_miniconda(targets):
        urlretrieve(url,miniconda_installer)

    return {'targets': [miniconda_installer],
            'uptodate': [True], # (as has no deps)
            'actions': [download_miniconda]}
############################################################
