#!/usr/bin/env python3
import json
import os
import subprocess
from sys import platform as _platform

HERE = os.path.dirname(os.path.abspath(__file__))
ADDON_DIR = os.path.join(HERE, 'add-on')


def write_native_app_json():
    data = {
        "name": "ping_pong",
        "description": "Example host for native messaging",
        "path": os.path.join(HERE, 'app', 'ping_pong.py'),
        "type": "stdio",
        "allowed_extensions": ["ping_pong@example.org"],
    }
    json_path = os.path.join(HERE, 'app', 'ping_pong.json')
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    return json_path


def create_native_manifest(json_path):
    if _platform == 'linux':
        dst_path = os.path.join(
            os.path.expanduser('~/.mozilla/'),
            'native-messaging-hosts',
            os.path.basename(json_path),
        )
    elif _platform == 'darwin':
        dst_path = os.path.join(
            os.path.expanduser('~/Library/Application Support/Mozilla'),
            'NativeMessagingHosts',
            os.path.basename(json_path),
        )
    else:
        raise RuntimeError(
            'This platform is not supported currently. You can manually setup the manifest '
            'using the instructions here: '
            'https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Native_manifests'
        )

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    if not os.path.exists(dst_path):
        os.link(json_path, dst_path)


def setup_extension():
    json_path = write_native_app_json()
    create_native_manifest(json_path)


def start_web_ext(executable, profile_dir):
    env = os.environ.copy()
    env['_MOZ_PROFILE_DIR'] = profile_dir
    try:
        subprocess.check_call(
            [
                'web-ext',
                'run',
                '-f',
                executable,
                '-p',
                profile_dir,
                '--keep-profile-changes',
            ],
            cwd=ADDON_DIR,
            env=env,
        )
    except Exception:
        pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Start a Firefox instance with this add-on enabled.'
    )
    parser.add_argument(
        '--firefox-binary',
        default='firefox',
        help='Name of (or path to) the Firefox binary',
    )
    parser.add_argument(
        '--profile-dir', help='Path to profile dir', required=True
    )
    args = parser.parse_args()
    setup_extension()
    start_web_ext(executable=args.firefox_binary, profile_dir=args.profile_dir)
