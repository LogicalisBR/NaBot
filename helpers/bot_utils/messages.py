import re
import shlex
from itertools import zip_longest

from flask import request

from webexteamssdk import Webhook
from .cards import initial_card, create_card_show_line, show_card, info_card, debug_card, backup_card, diff_card, \
    config_card
from ..nornir_helper import init, send_show_command, get_device_data, get_inventory_dict, get_config_backup, \
    get_config_diff, set_config
from ..os_helper import serve_file


def answer_message_received(teams_api, json_data):
    """ Process the message received and return something to user
    :param teams_api: WebexTeamsAPI class
    :param json_data: flask.request.json
    :return: None
    """

    # Pass the JSON data so that it can get parsed by the Webhook class
    webhook_obj = Webhook(json_data)

    # Obtain information about the request data such as room, message,
    # the person it came from and person's email address.
    room = teams_api.rooms.get(webhook_obj.data.roomId)
    message = teams_api.messages.get(webhook_obj.data.id)
    person = teams_api.people.get(message.personId)
    email = person.emails[0]

    print("NEW MESSAGE IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    # If th message was sent by the bot, do not respond.
    me = teams_api.people.me()
    if message.personId == me.id:
        print("IGNORING MY OWN MESSAGE \n")
        return 'OK'
    else:
        # Parse message here and answer
        supported_actions = ['/show', '/diff', '/backup', '/info', '/config', '/debug']
        message_params = shlex.split(message.text)
        user_action = message_params[0]
        if re.match(r'(^/).*', user_action) and any(user_action in action for action in supported_actions):
            if len(message_params) < 3 and '/show' in user_action:
                teams_api.messages.create(room.id, text='Incorrect input. Please send like: \n '
                                                        '/show <hostname> "<command>"\n '
                                                        'ex: /show iosxr1 "show ip int b"')

            elif len(message_params) < 3 and '/diff' in user_action:
                teams_api.messages.create(room.id, text='Incorrect input. Please send like: \n '
                                                        '/diff <hostname> "<configuration>"\n '
                                                        'ex: /show iosxr1 "interface Loo100'
                                                        '  description Sample description'
                                                        '  no shutdown')

            elif len(message_params) < 2:
                teams_api.messages.create(room.id, text='Incorrect input. Please send like: \n '
                                                        '/info <hostname> \n '
                                                        'ex: /info iosxr1')
            else:
                variables_params = ['action', 'hostname', 'command']
                dict_params = dict(zip_longest(variables_params, message_params))
                print(dict_params)
                answer_action(teams_api, room.id, user_action.strip('/'), hostname=dict_params['hostname'],
                              user_input=dict_params['command'])
        else:
            # attachment = create_card_show_line()
            teams_api.messages.create(room.id, text='Initial card', attachments=[initial_card()])
            teams_api.messages.create(room.id, text='You can also use the supported parameters: \n' + ', '.join(
                supported_actions) + '\n'
                                     'Example:\n'
                                     '/info <hostname>\n'
                                     '/show <hostname> "<command>"\n '
                                      )


def answer_attachment_received(teams_api, json_data):
    """Create and return another adaptative card to be sent everytime the bot receive an attachment webhook """

    # Pass the JSON data so that it can get parsed by the Webhook class
    webhook_obj = Webhook(json_data)

    room = teams_api.rooms.get(webhook_obj.data.roomId)
    attachment_action = teams_api.attachment_actions.get(webhook_obj.data.id)
    person = teams_api.people.get(attachment_action.personId)
    email = person.emails[0]

    message_id = attachment_action.messageId
    hostname = attachment_action.inputs.get('hostname', None)

    print("NEW ATTACHMENT IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE: '{}'\n".format(attachment_action))

    me = teams_api.people.me()
    if attachment_action.personId == me.id:
        print("IGNORING MY OWN MESSAGE \n")
        return 'OK'
    else:
        if attachment_action.inputs.get('ExecActionChoice', None):
            action = attachment_action.inputs.get('ExecActionChoice', None)
            hostname = attachment_action.inputs.get('hostname', None)
            show_command = attachment_action.inputs.get('command', None)

            answer_action(teams_api, room.id, action, hostname, show_command)
        elif attachment_action.inputs.get('InitialActionChoice', None):
            attachment = None
            action = attachment_action.inputs.get('InitialActionChoice', None)
            # Ask more information based on action received
            if action == 'show':
                attachment = show_card()
            elif action == 'info':
                attachment = info_card()
            elif action == 'debug':
                attachment = debug_card()
            elif action == 'backup':
                attachment = backup_card()
            elif action == 'diff':
                attachment = diff_card()
            elif action == 'config':
                attachment = config_card()

            if attachment is not None:
                teams_api.messages.create(room.id,
                                          text='Sendind execAction card',
                                          attachments=[attachment])


def send_custom_card(teams_api, json_data):
    """Create and return an adaptative card to be sent everytime the bot is mentioned """

    # Pass the JSON data so that it can get parsed by the Webhook class
    webhook_obj = Webhook(json_data)

    # Obtain information about the request data such as room, message,
    # the person it came from and person's email address.
    room = teams_api.rooms.get(webhook_obj.data.roomId)
    message = teams_api.messages.get(webhook_obj.data.id)
    person = teams_api.people.get(message.personId)
    email = person.emails[0]

    print("NEW MESSAGE IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    """ Insert your custom card here"""
    attachment = create_card_show_line()

    # If th message was sent by the bot, do not respond.
    me = teams_api.people.me()
    if message.personId == me.id:
        return 'OK'
    else:
        teams_api.messages.create(room.id, text='Custom Card', attachments=[attachment])


def send_initial_card(teams_api, json_data):
    """Create and return an adaptative card to be sent everytime the bot is mentioned """
    print('Preparing card to be returned. \r\n')

    # Pass the JSON data so that it can get parsed by the Webhook class
    webhook_obj = Webhook(json_data)

    # Obtain information about the request data such as room, message,
    # the person it came from and person's email address.
    room = teams_api.rooms.get(webhook_obj.data.roomId)
    message = teams_api.messages.get(webhook_obj.data.id)
    person = teams_api.people.get(message.personId)
    email = person.emails[0]

    print("NEW MESSAGE IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    # attachment = create_card_show_line()
    attachment = initial_card()

    # If th message was sent by the bot, do not respond.
    me = teams_api.people.me()
    if message.personId == me.id:
        print("IGNORING MY OWN MESSAGE \n")
        return 'OK'
    else:
        teams_api.messages.create(room.id, text='Initial card', attachments=[attachment])

def send_result_file(teams_api, roomId, hostname, result):
    import secrets
    import os
    filename = hostname + "_" + secrets.token_hex(nbytes=16) + ".txt"
    filename = serve_file(filename, result)
    teams_api.messages.create(roomId, files=[filename])
    os.remove(filename)


def answer_action(teams_api, roomId, action, hostname, user_input):

    try:
        if action == 'show':
            user_input = user_input.strip()
            user_input = user_input.lower()
            if user_input is not None and re.match(r'conf([a-z]*)\s+t([a-z]*).*', user_input) is None:
                print(f"Show command to send: {user_input}")
                result = send_show_command(hostname, user_input)
                if result is not None:
                    result = result[hostname].result
                    msg = f'Info on Device:\n{result}'
                    if len(result) > 6500:
                        msg = "Output is too large. Returning as a file."
                teams_api.messages.create(roomId, text=msg)
                send_result_file(teams_api, roomId, hostname, result)
            else:
                teams_api.messages.create(roomId, text='Invalid show command')

        elif action == 'diff':
            result = get_config_diff(hostname, user_input)
            for ansi_block, html_block in {"\033[91m": '',  # Red
                                           "\033[92m": '! ----- ----- ----- ----- ----- ----- ',  # Green
                                           "\033[93m": '! ----- ----- ----- Candidate Block ----- ----- ',  # Yellow
                                           "\033[0m": ""}.items():
                result = result.replace(ansi_block, html_block)
            msg = f'Device diff configuration:\n{result}'
            teams_api.messages.create(roomId, text=msg)
            send_result_file(teams_api, roomId, hostname, result)

        elif action == 'config':
            result, loaded_cfg = set_config(hostname, user_input)
            # AggregatedResult (cfg_commit_config): {'csr1000v-1': MultiResult: [ScrapliResult: "cfg_commit_config"]}
            if result.failed is False:
                # result[hostname].scrapli_response.scrapli_responses
                msg = f'Device configuration result: \n SUCCESSFULLY APPLIED:\n{user_input}'
                teams_api.messages.create(roomId, text=msg)
                result = get_config_backup(hostname)
                result = result[hostname].result
                send_result_file(teams_api, roomId, hostname, result)
            else:
                msg = f"Device configuration result: \n FAILED TO APPLY:\n Device returned one of: '% Ambiguous command', '% Incomplete command', '% Invalid input detected', '% Unknown command'"
                teams_api.messages.create(roomId, text=msg)

        elif action == 'info':
            result = get_device_data(hostname)
            msg = f'Device IP info :\n{result}'
            teams_api.messages.create(roomId, text=msg)

        elif action == 'debug':
            result = get_inventory_dict(hostname)
            if result[hostname].get('password'):
                result[hostname].pop('password')
            msg = f'Device NetBox info :\n{result}'
            teams_api.messages.create(roomId, text=msg)

        elif action == 'backup':
            result = get_config_backup(hostname)
            result = result[hostname].result
            msg = f'Device NetBox info :\n{result}'
            if result is not None:
                if len(result) > 6500:
                    msg = "Output is too large. Returning as a file."
                teams_api.messages.create(roomId, text=msg)
                send_result_file(teams_api, roomId, hostname, result)
            else:
                msg = "Failed to execute. Please verify the device name, if it's reachable, correctly registered in NetBox.\n"
                teams_api.messages.create(roomId, text=msg)
        else:
            teams_api.messages.create(roomId, text='Not implemented',
                                      attachments=[show_card()])
    except Exception as e:
        print(e)
        msg = "Failed to execute. Please verify the device name, if it's reachable, correctly registered in NetBox.\n"
        teams_api.messages.create(roomId, text=msg)
