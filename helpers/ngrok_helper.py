import json
import requests

__all__ = ['get_ngrok_url']


def get_ngrok_url(addr='127.0.0.1', port=4040):
    url = requests.get(f"http://{addr}:{port}/api/tunnels").json()['tunnels'][0]['public_url']
    return url
