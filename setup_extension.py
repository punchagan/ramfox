#!/usr/bin/env python3
import json
import os
from sys import platform as _platform

HERE = os.path.dirname(os.path.abspath(__file__))


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


if __name__ == '__main__':
    json_path = write_native_app_json()
    create_native_manifest(json_path)
