#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# 3rd party imports ------------------------------------------------------------
# Flask help can be found here:
# http://flask.pocoo.org/
from flask import Flask, request, jsonify

# local imports ----------------------------------------------------------------
from webexteamssdk import WebexTeamsAPI
from helpers import (read_yaml_data,
                     get_ngrok_url)
from helpers.webhook_helper import create_webhook_message, create_webhook_attachments
from helpers.bot_utils import messages

flask_app = Flask(__name__)
teams_api = None


# A python decorator which tells Flask to execute this method when the uri is hit
# and the HTTP method is a "POST" request. 
@flask_app.route('/webhook/message', methods=['POST'])
def webhook_message_received():
    # Only execute this section of code when a POST request is sent, as a POST indicates that a message
    # has been received and needs processing.
    if request.method == 'POST':
        print('Received a new message...')
        messages.answer_message_received(teams_api, request.json)
    else:
        print('received none post request, not handled!')
    return 'OK'


@flask_app.route('/webhook/attachment', methods=['POST'])
def webhook_attachment_received():
    if request.method == 'POST':
        messages.answer_attachment_received(teams_api, request.json)
    else:
        print('received none post request, not handled!')
    return 'OK'



if __name__ == '__main__':
    # Read the configuration that contains the bot access token
    config = read_yaml_data('/opt/config/config.yaml')['nabot']

    teams_api = WebexTeamsAPI(access_token=config['teams_access_token'])

    # Get some required NGrok information
    ngrok_url = get_ngrok_url()

    # Register ngrok_url created at Webex.com to receive notifications for new messages/events
    create_webhook_message(teams_api, ngrok_url)
    create_webhook_attachments(teams_api, ngrok_url)

    # Host flask web server on port 5000
    flask_app.run(host='0.0.0.0', port=5000)
