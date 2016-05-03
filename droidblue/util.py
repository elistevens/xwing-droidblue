import re

canonicalizationExceptions_dict = {
    "Astromech Droid": "amd",
    "Salvaged Astromech Droid": "samd",
    "Elite Pilot Talent": "ept",
    "Modification": "mod",
}


def canonicalize(name):
    if name in canonicalizationExceptions_dict:
        return canonicalizationExceptions_dict[name]

    return re.sub('[^a-z0-9]', '', name.lower())


def importstr(module_str, from_=None):
    """
    >>> importstr('os')
    <module 'os' from '.../os.pyc'>
    >>> importstr('math', 'fabs')
    <built-in function fabs>
    """
    module = __import__(module_str)
    for sub_str in module_str.split('.')[1:]:
        module = getattr(module, sub_str)

    if from_:
        try:
            return getattr(module, from_)
        except:
            raise ImportError('{}.{}'.format(module_str, from_))
    return module
