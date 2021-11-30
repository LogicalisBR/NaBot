from helpers import find_webhook_by_name, delete_webhook, create_webhook


def clean_webhooks_url(teams_api, webhook_name):
    # is important to reconfigure the ngrok url at every application restart
    dev_webhook = find_webhook_by_name(teams_api, webhook_name)
    if dev_webhook:
        delete_webhook(teams_api, dev_webhook)


def create_webhook_message(teams_api, ngrok_url):
    # This webhook will listen for new messages

    # Define the name of webhook
    webhook_name = 'webhook-messages'

    # Find any existing webhooks with this name and if already exists, delete it
    clean_webhooks_url(teams_api, webhook_name)

    # Create a new teams webhook with the name defined above and the current public ngrok url
    create_webhook(teams_api, webhook_name, ngrok_url + '/webhook/message')


def create_webhook_attachments(teams_api, ngrok_url):
    # This webhook will listen for events on adaptativeCards responses

    # Define the name of webhook
    webhook_name = 'webhook-attachments'

    # Find any existing webhooks with this name and if this already exists then delete it
    clean_webhooks_url(teams_api, webhook_name)

    # Create a new teams webhook with the name defined above and the current public ngrok url
    # adaptativeCards responses are sent as attachments
    create_webhook(teams_api, webhook_name, ngrok_url + '/webhook/attachment', resource='attachmentActions',
                   event='created')
