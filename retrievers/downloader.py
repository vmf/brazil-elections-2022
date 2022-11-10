import urllib.request
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_file(url, output_path, overall_desc=""):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=overall_desc + url.split('/')[-1]) as t:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'MyApp/1.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

