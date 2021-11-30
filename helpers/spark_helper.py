__all__ = ['delete_webhook', 'delete_all_webhook',
           'find_webhook_by_name', 'create_webhook']


def delete_webhook(api, webhook):
    api.webhooks.delete(webhook.id)


def delete_all_webhook(api):
    hooks = api.webhooks.list()
    for hook in hooks:
        api.webhooks.delete(hook.id)


def find_webhook_by_name(api, name):
    webhooks = api.webhooks.list()
    for hook in webhooks:
        if hook.name == name:
            return hook
    return False

def create_webhook(api, name, target_url,
                   resource='messages',
                   event='created',
                   filter=None):
    res = api.webhooks.create(name=name,
                              targetUrl=target_url,
                              resource=resource,
                              event=event,
                              filter=filter)
    return res
