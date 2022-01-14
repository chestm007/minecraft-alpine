from github import Github
import urllib.request
import sys

repos = {
    'fabric-carpet': 'gnembon/fabric-carpet',
    'carpet-extra': 'gnembon/carpet-extra',
    'carpet-autocraftingtable': 'gnembon/carpet-autoCraftingTable'
}


def main(in_ver):
    print(f'finding carpet mods for minecraft version: {in_ver}')
    g = Github('a5903089fb8cae6f22334d2f561f8fe0647a328a')
    versions = {}
    print('scanning repos...')
    for n, repo in repos.items():
        print(f'scanning repo: {n}')
        r = g.get_repo(repo)
        for release in r.get_releases():
            for asset in release.get_assets():
                try:
                    # sanitise asset name to be just {mc version}-{carpet version}
                    version_matrix = asset.name.lower().split(n + '-')[1].split('.jar')[0].split("+")[0].split('_')[0]
                except IndexError:
                    print('error processing: "' + asset.name + '"')
                    continue

                # filter out snapshot builds
                strings = ('w', 'experimental', 'snapshot', 'rc', 'pre', 'v')
                if any(s in version_matrix for s in strings):
                    continue

                try:
                    mc_ver, carpet_ver = version_matrix.split('-')
                except ValueError:
                    print(f'issue decoding {n} version from string: {version_matrix}')
                    continue

                if mc_ver not in versions.keys():
                    versions[mc_ver] = {}

                if carpet_ver not in versions[mc_ver]:
                    versions[mc_ver][carpet_ver] = {n: asset}
                else:
                    versions[mc_ver][carpet_ver][n] = asset

    print('computing compatible versions...')
    full_compat_versions = {}
    for mc_ver, fabrics in versions.items():
        for fabric_ver, mods in fabrics.items():
            if sorted(list(repos.keys())) == sorted(list(mods.keys())):
                full_compat_versions[mc_ver] = mods
                break

    if full_compat_versions.get(in_ver):
        for name, mod in full_compat_versions.get(in_ver).items():
            print(f'downloading: {name}')
            urllib.request.urlretrieve(mod.browser_download_url, f'temp_dir/mods/{name}.jar')
            print(mod.browser_download_url)
        return True

    print(f'cannot find carpet mods for version: {in_ver}')


if __name__ == '__main__':
    if main(sys.argv[1:][0]):
        sys.exit(0)
    sys.exit(1)
