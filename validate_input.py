import argparse
import os
import requests
import subprocess


def is_valid_directory_type(directory_type):
    """Verifies that directory type is plugin or theme"""
    valid_types = ['plugins', 'themes']
    return directory_type in valid_types


def is_valid_slug(url):
    """Verifies that slug exists in the chosen directory"""
    r = requests.get(url)
    return r.status_code == 200


def is_unknown_version(url, version):
    """Verifies that version does not already exist in the svn repository"""
    r = requests.get("{}/tags/{}".format(url, version))
    return r.status_code != 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a plugin or theme to the wordpress.org directory')
    parser.add_argument('directory_type', type=str,
                        help='can be "plugins" or "themes"')
    parser.add_argument('slug', type=str,
                        help='theme or plugin slug')
    parser.add_argument('version', type=str,
                        help='theme or plugin version')
    parser.add_argument('username', type=str,
                        help='wordpress.org username')
    parser.add_argument('password', type=str,
                        help='wordpress.org password')
    args = parser.parse_args()
    svn_url = 'https://{}.svn.wordpress.org/{}'.format(args.directory_type, args.slug)

    if not is_valid_directory_type(args.directory_type):
        raise ValueError('Invalid directory type: wordpress.org directory type can be "plugins" or "themes"')

    if not is_valid_slug(svn_url):
        raise ValueError("{} does not exist in the {} directory".format(args.slug, args.directory_type))

    if not is_unknown_version(svn_url, args.version):
        raise ValueError("{} version {} already exists in the {} directory".format(args.slug, args.version, args.directory_type))

    app_dir = os.environ['APP_DIR']
    upload_cmd = ['{}/upload_to_svn.sh'.format(app_dir), svn_url, args.version, args.username, args.password]
    subprocess.run(upload_cmd)
