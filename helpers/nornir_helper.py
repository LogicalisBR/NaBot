from nornir_scrapli.functions import print_structured_result
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import cfg_load_config, cfg_diff_config, cfg_commit_config
from nornir_netbox.plugins.inventory.netbox import NetBoxInventory2
from nornir_utils.plugins.functions import print_result
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.plugins.inventory import TransformFunctionRegister
from nornir.core.inventory import ConnectionOptions
from nornir.core.task import Task, Result
from nornir.core.filter import F
from nornir import InitNornir
from pprint import pprint
import argparse
import os


def convert_host_data(host):
    """
    Transform function to turn serialized objects from Netbox into nornir Hosts 
    with corresponding parameters:
        + username
        + password
        + port
        + platform
        + connection_options (disable strict key checking)

    The function set_secret_credentials can be used to obtain
    secrets from a vault for different device categories
    """
    host.port = 22
    if host.name == 'iosxr1':
        # Credentials for always-on devnet SandBox
        host.username = "admin"
        host.password = "C1sco12345"
    elif host.name == 'csr1000v-1':
        # Credentials for always-on devnet SandBox
        host.username = "developer"
        host.password = "C1sco12345"

    # This disables strict key checking to ignore the first-login fingerprint validation
    # from the CLI
    if host.data.get('platform'):
        host.platform = host.data["platform"]["display"]
        if host.data["platform"]["display"] in ['cisco_ios', 'cisco_iosxe', 'cisco_iosxr']:
            host.connection_options["scrapli"] = ConnectionOptions(
                extras={
                    "auth_strict_key": False
                }
            )

CONFIG_FILE = '/opt/config/nornir_config.yaml'
InventoryPluginRegister.register("netbox_inventory", NetBoxInventory2)
TransformFunctionRegister.register("convert_host_data", convert_host_data)


def get_inventory_dict(hostname):
    """
    Return a dictionary with host data known to Nornir object nr
    """
    nr = init(hostname_filter=hostname)
    return nr.inventory.dict()['hosts']


def get_config_backup(hostname):
    """
    Return configuration backup for a given nornir object
    """
    config = send_show_command(hostname, "show running-config")
    return config


def get_device_data(hostname):
    """
    Returns sample data on host as obtain from netbox
    Returns output string with hostname and IP address of Device
    """
    nr = init(hostname_filter=hostname)
    output_string = ""
    hostdict = nr.inventory.dict()['hosts']
    # Check if no host was specified
    if not hostdict:
        output_string += "No device found. Please review hostname."

    for host in hostdict.keys():
        output_string += "----------------------------\n"
        output_string += "Hostname:    {}\n".format(host)
        output_string += " IP Address: {}\n".format(hostdict[host]['hostname'])

    return output_string


def get_config_diff(hostname, candidate_config):
    """
    Returns a dry-run (diff) running config on device and candidate config.
    + nr is a Nornir object
    + candidate_config is a multi-line string with configs one wishes to apply
    """
    nr = init(hostname_filter=hostname)
    hosts = [host for host in nr.inventory.hosts.keys()]
    sanitized_candidate = [item.rstrip() for item in candidate_config.splitlines() if item]
    candidate = "\n".join(item for item in sanitized_candidate) + "\n"
    nr.run(
        task=cfg_load_config,
        config=candidate)

    diff = nr.run(
        task=cfg_diff_config,
        source="running")

    output_diff = "=======================\n".join(diff[host].scrapli_response.side_by_side_diff for host in hosts)

    return output_diff


def set_config(hostname, candidate_config):
    """
    Returns a dry-run (diff) running config on device and candidate config. Also applies config to the Device with
    Scrapli_cfg

    + nr is a Nornir object
    + candidate_config is a multi-line string with configs one wishes to apply
    """
    nr = init(hostname_filter=hostname)

    load_cfg = nr.run(
        task=cfg_load_config,
        config=candidate_config)

    result = nr.run(
        task=cfg_commit_config,
        source="running"
    )

    return result, load_cfg


def send_show_command(hostname, show_command):
    """
    Executes Nornir Task send_command from nornir_scrapli.
    TODO: Implement a flag to determine whether or not the result is to be parsed
    """
    nr = init(hostname_filter=hostname)
    results = nr.run(
        task=send_command,
        command=show_command)

    return results


def init(hostname_filter: str):
    """
    Return nornir object with hostname_filter applied, "all" will return all the devices
    in the inventory.
    """
    nr = InitNornir(config_file=CONFIG_FILE)
    # if hostname_filter == "all":
    # return nr
    filtered = nr.filter(F(name=hostname_filter))
    return filtered


# The script can be run from the CLI to test some functions
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nornir Netbox Helper CLI")
    parser.add_argument(
        "hostname",
        type=str,
        help="Target hostname on inventory. 'all' will apply to the whole inventory.")

    parser.add_argument(
        "-i",
        "--inventory",
        action="store_true",
        help="Print Dynamic Inventory",
        required=False)

    parser.add_argument(
        "-e",
        "--exec",
        nargs="?",
        help="Execute EXEC mode command on device",
        required=False)

    parser.add_argument(
        "-b",
        "--backup",
        action="store_true",
        help="Run configuration Backup",
        required=False)

    parser.add_argument(
        "-d",
        "--dry-run",
        nargs="?",
        help="Compare given config with running config",
        required=False)

    parser.add_argument(
        "-c",
        "--config",
        nargs="?",
        help="Merge given config with running config",
        required=False)

    args = vars(parser.parse_args())
    target_host = args['hostname']
    print(f"Target host is {target_host}")

    # Print inventory dict without secret
    if args["inventory"]:
        nr = init(hostname_filter=target_host)
        device_info = nr.inventory.hosts[target_host].dict()
        device_info.pop('password')
        pprint(device_info)

    # Run Show command on device with scrapli
    elif args["exec"]:
        command = args['exec']
        result = send_show_command(target_host, command)
        print_result(result)

    # Run configuration backup on device
    elif args["backup"]:
        result = get_config_backup(target_host)
        print_result(result)

    # Run configuration dry-run on device
    elif args["dry_run"]:
        result = get_config_diff(target_host, args["dry_run"])
        print(result)

    # Run configuration backup on device
    elif args["config"]:
        result = set_config(target_host, args["config"])
        print(result)
