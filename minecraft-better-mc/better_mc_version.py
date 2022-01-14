import json
import os
import sys
import urllib.request
from multiprocessing.pool import ThreadPool

from retry import retry

import requests
from zipfile import ZipFile

files_url = 'https://curse.nikky.moe/api/addon/{project_id}/files'


@retry(LookupError, delay=5, tries=3)
def better_mc_file_list():
    """
    dict_keys(['id', 'displayName', 'fileName', 'fileDate', 'releaseType',
               'fileStatus', 'downloadUrl', 'isAlternate', 'alternateFileId',
               'dependencies', 'isAvailable', 'modules', 'packageFingerprint',
               'gameVersion', 'installMetadata', 'serverPackFileId', 'fileLength'])
    :return: 
    """
    response = requests.get(files_url.format(project_id=452013))
    if response.status_code == 200:
        return response.json()
    else:
        raise LookupError()


def get_better_mc_zip(in_version):
    better_mc_versions = {}

    def parse_mod_version(display_name):
        return display_name.split('v')[-1].split(' ')[0]

    for f in better_mc_file_list():
        for game_version in f.get('gameVersion'):
            if game_version.lower() in ('fabric', 'forge'):
                continue
            if 'snapshot' in game_version.lower():
                continue

            mod_version = float(parse_mod_version(f.get('displayName')))
            try:
                better_mc_versions[game_version][mod_version] = f
            except KeyError:
                better_mc_versions[game_version] = {mod_version: f}

    better_mc = better_mc_versions[in_version][max(v for v in better_mc_versions[in_version])]

    zip_file_path = f'temp_dir/{better_mc.get("fileName")}'
    urllib.request.urlretrieve(better_mc.get('downloadUrl').replace(' ', '%20'), zip_file_path)
    with ZipFile(zip_file_path) as bmczip:
        # iterate over files in zipfile/overrides and extract to the folders
        for file in bmczip.namelist():
            if file.startswith('overrides/'):
                with bmczip.open(file, 'r') as z_file:
                    file = file.replace('overrides/', '')
                    print(f'extracting {file}')
                    if not file:
                        continue
                    location = f'temp_dir/{file}'
                    try:
                        with open(location, 'wb') as d_file:
                            d_file.write(z_file.read())
                    except IsADirectoryError:
                        try:
                            os.mkdir(location)
                        except FileExistsError:
                            continue

        with bmczip.open('manifest.json') as manifest:
            manifest_json = json.load(manifest)

            p = ThreadPool(30)
            results = p.map(get_mod, manifest_json.get('files'))
            p.close()
            p.join()

            p = ThreadPool(20)
            p.map(download_mod, results)
            p.close()
            p.join()


def download_mod(mod):
    if mod is None:
        return
    print(f'Downloading mod: {mod.get("displayName")} | {mod.get("downloadUrl")}')
    mod_file_path = f'temp_dir/mods/{mod.get("fileName")}'
    data = requests.get(mod.get('downloadUrl').replace(' ', '%20'))
    with open(mod_file_path, 'wb') as mf:
        mf.write(data.content)


@retry(LookupError, delay=5, tries=10)
def get_mod(f):
    response = requests.get(files_url.format(project_id=f.get('projectID')))
    if response.status_code == 200:
        for m in response.json():
            if m['id'] == f.get('fileID'):
                return m

        print(f"{response.json()[0].get('displayName')}: file couldnt be found.")

    else:
        raise LookupError()


def main(in_version):
    print(get_better_mc_zip(in_version))


if __name__ == '__main__':
    main(sys.argv[1:][0])