import pynetbox
from slugify import slugify

from yaml_helper import read_yaml_data

netbox_inventory_config = read_yaml_data('../config/nornir_config.yaml')['inventory']
netbox_api_url = netbox_inventory_config['options']['nb_url']
netbox_api_token = netbox_inventory_config['options']['nb_token']

nb = pynetbox.api(
    url=netbox_api_url,
    token=netbox_api_token)


def assert_site(device_data):
    site_slug = slugify(device_data['site'])
    dev_site = nb.dcim.sites.get(slug=site_slug)
    if dev_site == None:
        dev_site = nb.dcim.sites.create({
            "name": device_data['site'],
            "slug": site_slug
        }
        )
    else:
        print("Site already exists. Skipping...")

    return dev_site


def assert_tenant(device_data):
    tenant_slug = slugify(device_data['tenant'])
    dev_tenant = nb.tenancy.tenants.get(slug=tenant_slug)
    if dev_tenant == None:
        dev_tenant = nb.tenancy.tenants.create({
            "name": device_data['tenant'],
            "slug": tenant_slug})
    else:
        print("Site already exists. Skipping...")

    return dev_tenant


def assert_platform(device_data):
    manufacturer_slug = slugify(device_data['platform']['manufacturer'])
    dev_manufacturer = nb.dcim.manufacturers.get(slug=manufacturer_slug)
    if dev_manufacturer == None:
        dev_manufacturer = nb.dcim.manufacturers.create({
            "name": device_data['platform']['manufacturer'],
            "slug": manufacturer_slug})
    else:
        print("Site already exists. Skipping...")

    name_slug = slugify(device_data['platform']['name'])
    print(name_slug)
    dev_platform = nb.dcim.platforms.get(slug=name_slug)
    if dev_platform == None:
        dev_platform = nb.dcim.platforms.create({
            "name": device_data['platform']['name'],
            "slug": name_slug,
            "manufacturer": dev_manufacturer.id
        })
    else:
        print("Site already exists. Skipping...")

    return dev_manufacturer, dev_platform


def assert_type(device_data, manufacturer):
    type_slug = slugify(device_data['type']['name'])
    dev_type = nb.dcim.device_types.get(slug=type_slug)
    if dev_type == None:
        dev_type = nb.dcim.device_types.create({
            "name": device_data['type']['name'],
            "slug": type_slug,
            "model": device_data['type']['name'],
            "manufacturer": manufacturer.id})
    else:
        print("Device Type already exists. Skipping...")

    return dev_type


def assert_role(device_data):
    role_slug = slugify(device_data['role'])
    dev_role = nb.dcim.device_roles.get(slug=role_slug)
    if dev_role == None:
        dev_role = nb.dcim.device_roles.create({
            "name": device_data['role'],
            "slug": role_slug})
    else:
        print("Device Role already exists. Skipping...")

    return dev_role


def add_interface(interface, device_data):
    iface_name = interface
    iface = nb.dcim.interfaces.get(
        name=iface_name,
        device=device_data['name']
    )

    device = nb.dcim.devices.get(name=device_data['name'])

    if iface == None:
        iface = nb.dcim.interfaces.create({
            "name": iface_name,
            "device": device.id,
            "type": "other"
        })
    else:
        print("Interface already exists. Skipping...")
    return iface


def add_ip_address(interface, device_data):
    device = nb.dcim.devices.get(name=device_data['name'])

    # Check if Interface exists
    iface = nb.dcim.interfaces.get(
        name=interface.name,
        device=device_data['name'])

    ip_addr = nb.ipam.ip_addresses.create(
        address=device_data['interfaces'][interface.name]['ipv4_address'],
        assigned_object_type="dcim.interface",
        assigned_object_id=interface.id,
        status="active")

    if device_data['interfaces'][interface.name]['primary'] == True:
        nb.dcim.devices.update([
            {'id': device.id, 'primary_ip4': ip_addr.id}])

    return ip_addr


def add_device(device_data):
    """
    Adds a device on Netbox from a dictionary. Test that mandatory values exist, 
    if not, create them
    """
    # Make sure required objects already exist
    dev_site = assert_site(device_data)
    print("finished site")
    dev_tenant = assert_tenant(device_data)
    print("finished tenant")
    dev_manufacturer, dev_platform = assert_platform(device_data)
    print("finished platform")
    dev_type = assert_type(device_data, dev_manufacturer)
    print("finished type")
    dev_role = assert_role(device_data)
    print("finished role")

    # Add device proper
    device = nb.dcim.devices.get(name=device_data['name'])
    if device == None:
        device = nb.dcim.devices.create({
            "name": device_data['name'],
            "device_type": dev_type.id,
            "device_role": dev_role.id,
            "site": dev_site.id,
            "platform": dev_platform.id,
            "tenant": dev_tenant.id})
    else:
        print("Device already exists. Skipping...")

    iface_list = []
    # Add device interface
    for interface in device_data['interfaces']:
        iface_list.append(add_interface(interface, device_data))

    # Add device IP address
    for iface in iface_list:
        add_ip_address(iface, device_data)


if __name__ == '__main__':
    devices_data = read_yaml_data('../config/devices.yaml')
    for host in devices_data['devices']:
        add_device(host)
