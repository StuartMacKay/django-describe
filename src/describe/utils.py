from django.conf import settings


def get_settings(metadata, key='settings'):
    """
    Generate a dict containing all Django settings and add it to the target dict.

    Args:
        metadata: The dictionary to add settings to
        key: The key to use for the settings dict (default: 'settings')

    Returns:
        The modified metadata dict
    """
    settings_dict = {}

    for setting in dir(settings):
        if setting.isupper():
            settings_dict[setting] = getattr(settings, setting)

    metadata[key] = settings_dict
    return metadata
