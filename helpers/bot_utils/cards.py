from pyadaptivecards.actions import Submit, OpenUrl
from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.components import TextBlock, Image, Choice, Column
from pyadaptivecards.container import ColumnSet
from pyadaptivecards.inputs import Text, Choices
from pyadaptivecards.options import ImageSize


def initial_card():
    # Create card components
    # See https://pyadaptivecards.readthedocs.io/en/latest/modules.html#components

    # Configuring an header with a logo image properties as location, size
    header_set = create_card_header()

    # Configuring extra fields in the card
    greeting = TextBlock("Select one option below to continue.")

    exec_cmd = Submit(data={"InitialActionChoice": "show"}, title="SHOW: Execute a 'show' command.")
    diff = Submit(data={"InitialActionChoice": "diff"}, title="DIFF: Input a candidate config and see the diff.")
    backup = Submit(data={"InitialActionChoice": "backup"}, title="BACKUP: Get a file with the running-config.")
    info = Submit(data={"InitialActionChoice": "info"}, title="INFO: Retrieve device IP information.")
    config = Submit(data={"InitialActionChoice": "config"}, title="CONFIG: Configure a device.")
    # debug = Submit(data={"InitialActionChoice": "debug"}, title="DEBUG: Retrieve device information on NetBox.")

    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting],
                        actions=[exec_cmd, info, backup, diff, config]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def show_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname")
    hostname = Text('hostname', placeholder="Device Hostname")
    command = Text('command', placeholder="ex: show ip int brief")

    exec_cmd = Submit(data={"ExecActionChoice": "show"}, title="Execute a 'show' command.")

    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting,hostname,  command],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def info_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname:")
    hostname = Text('hostname', placeholder="Device Hostname")
    exec_cmd = Submit(data={"ExecActionChoice": "info"}, title="Get IP Address")
    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting, hostname],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def debug_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname:")
    hostname = Text('hostname', placeholder="Device Hostname")
    exec_cmd = Submit(data={"ExecActionChoice": "debug"}, title="Get all device information")
    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting, hostname],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def backup_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname:")
    hostname = Text('hostname', placeholder="Device Hostname")
    exec_cmd = Submit(data={"ExecActionChoice": "backup"}, title="Perform device backup and print result.")
    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting, hostname],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def diff_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname:")
    hostname = Text('hostname', placeholder="Device hostname")
    command = Text('command', placeholder="ex: ntp x.x.x.x", isMultiline=True)
    exec_cmd = Submit(data={"ExecActionChoice": "diff"}, title="Perform device diff with the config supplied and print result.")
    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting, hostname, command],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def config_card():
    # Placing header
    header_set = create_card_header()
    # Configuring extra fields in the card
    warning = TextBlock("WARNING: THIS OPTION WILL CONFIGURE THE DEVICE!")
    greeting = TextBlock("Input device Hostname:")
    hostname = Text('hostname', placeholder="Device hostname")
    command = Text('command', placeholder="ex: ntp x.x.x.x", isMultiline=True)
    exec_cmd = Submit(data={"ExecActionChoice": "config"},
                      title="Try to configure the device with the text supplied and print the result.")
    # Assemble the card
    card = AdaptiveCard(body=[header_set, warning, greeting, hostname, command],
                        actions=[exec_cmd]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

def create_card_show_line():
    attachment = create_card_enter_line(t_action="SHOW", t_command="ex: show running-config")
    return attachment


def create_card_config_diff_multiline():
    attachment = create_card_enter_multiline(t_action="CONFIG_DIFF", t_command="ex: ntp x.x.x.x")
    return attachment


def create_card_toggle():
    # Create card components
    # data:image/png;base64,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
    greeting = TextBlock("Input device Hostname")
    hostname = Text('hostname', placeholder="Device Hostname")

    show_toggle = Choice('SHOW', value='EXEC')
    info_toggle = Choice('SHOW', value='INFO')
    bkp_toggle = Choice('SHOW', value='BACKUP')
    action_set = Choices('action_set', choices=[show_toggle, info_toggle, bkp_toggle])

    submit = Submit(title="Send me!")

    card = AdaptiveCard(body=[greeting, hostname, action_set], actions=[submit])
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }


def create_card_header():
    open_url = OpenUrl("https://www.la.logicalis.com/pt-latam/", title="Logicalis Brazil")
    logo = Image("https://imagine.la.logicalis.com/hubfs/Logicalis-Favicon.png",
                 altText="Welcome to Logicalis NaBot.",
                 selectAction=open_url,
                 height="50px",
                 size=ImageSize(3)
                 )
    logo_cols = Column(items=[logo], width="auto")

    # Setting some text to display in lines
    first_line = TextBlock("Logicalis BR - NaBot", weight='3', size='3')
    second_line = TextBlock("Network Assistant Bot is part of Nep@l Solutions.", weight='2', size='1')
    nepal_url = "https://www.la.logicalis.com/pt-Latam/noticias/logicalis-apresenta-nepl-para-simplificar-a-adocao-de-redes-programaveis/"
    open_nepal_url = OpenUrl(nepal_url, title="Nep@l Services")
    line_cols = Column(items=[first_line, second_line], width="stretch", selectAction=open_nepal_url)

    # Assembly it all
    header_set = ColumnSet(columns=[logo_cols, line_cols], id="header_set")
    return header_set


def create_card_enter_multiline(t_action, t_command):
    # Create card components
    greeting = TextBlock("Input device Hostname")
    hostname = Text('hostname', placeholder="Device Hostname")
    action = Text('action', placeholder=t_action)
    command = Text('command', placeholder=t_command, isMultiline=True)

    submit = Submit(title="Send me!")

    card = AdaptiveCard(body=[greeting, hostname, action, command], actions=[submit])
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment


def create_card_enter_line(t_action, t_command):
    # Create card components
    #
    # Configuring an header with a logo image properties as location, size
    header_set = create_card_header()

    # Configuring extra fields in the card
    greeting = TextBlock("Input device Hostname")
    hostname = Text('hostname', placeholder="Device Hostname")

    exec_cmd = Submit(data={"InitialActionChoice": "show"}, title="Execute a 'show' command.")
    info = Submit(data={"InitialActionChoice": "info"}, title="Retrieve device IP information.")
    backup = Submit(data={"InitialActionChoice": "backup"},
                    title="Do a config backup and print it on the Webex channel.")

    # Assemble the card
    card = AdaptiveCard(body=[header_set, greeting, hostname],
                        actions=[exec_cmd, info, backup]
                        )
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": card.to_dict(),
    }
    return attachment

