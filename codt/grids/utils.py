def get_tuple_from_config(config, section, name, type):
    s = config.get(section, name)
    return tuple(int(v) for v in s.split(','))
