from django.urls import resolve, get_script_prefix


def _remove_prefix(path):
    if not path.endswith('/'):
        path += '/'

    script_name = get_script_prefix()
    if script_name:
        path = path.split(script_name, 1)[1]

    if not path.startswith('/'):
        path = '/' + path

    return path


def resolve_with_prefix(path):
    return resolve(_remove_prefix(path))
