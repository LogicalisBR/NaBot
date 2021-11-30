import yaml

__all__ = ['write_yaml_data', 'read_yaml_data']


def write_yaml_data(fpath, data):
    yaml_dump = yaml.dump(data, default_flow_style=False)
    with open(fpath, 'wb') as fh:
        fh.write(yaml_dump)


def read_yaml_data(fpath):
    with open(fpath, 'r') as ymlfile:
        data = yaml.safe_load(ymlfile)
    return data
