#!/usr/bin/env python3

import json
import os
import struct
import subprocess
import sys


# Python 3.x version
# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    return json.loads(message)


# Encode a message for transmission,
# given its content.
def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}


# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()


def open_url(url):
    """Open the URL in the default Firefox instance.

    We need to clear out some of the envvars before trying to start Firefox,
    since this process is started by Firefox as a native messaging process, and
    some weird flags can be turned on, which cause problems with opening the
    link.

    """
    environ = os.environ.copy()
    for key in os.environ.keys():
        if key.startswith('MOZ'):
            environ.pop(key)
    subprocess.check_call(['firefox-trunk', '--new-tab', url], env=environ)


while True:
    receivedMessage = getMessage()
    if receivedMessage == "ping":
        sendMessage(encodeMessage("pong3"))
    else:
        try:
            message = json.loads(receivedMessage)
        except ValueError:
            sendMessage(encodeMessage("Could not parse message"))
        else:
            url = message['url']
            sendMessage(encodeMessage('Opening page ({}) in default browser'.format(url)))
            open_url(url)
