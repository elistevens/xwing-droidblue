import json
import re

from .logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

canonicalizationExceptions_dict = {
    "Astromech Droid": "amd",
    "Salvaged Astromech Droid": "samd",
    "Elite Pilot Talent": "ept",
    "Modification": "mod",
}


def canonicalize(name):
    # if name in canonicalizationExceptions_dict:
    #     return canonicalizationExceptions_dict[name]

    return re.sub('[^a-z0-9_]', '', name.replace('-', '_').lower())


def importstr(module_str, from_=None):
    """
    >>> importstr('os')
    <module 'os' from '.../os.pyc'>
    >>> importstr('math', 'fabs')
    <built-in function fabs>
    """
    if from_ is None and ':' in module_str:
        module_str, from_ = module_str.rsplit(':')

    module = __import__(module_str)
    for sub_str in module_str.split('.')[1:]:
        module = getattr(module, sub_str)

    if from_:
        try:
            return getattr(module, from_)
        except:
            raise ImportError('{}.{}'.format(module_str, from_))
    return module


class Jsonable(object):
    jsonAttr_set = set()
    jsonSkip_set = set()

    @staticmethod
    def _object_hook(json_dict):
        log.debug([type(json_dict), repr(json_dict)])
        if '_cls' in json_dict:
            actual_str = json_dict.pop('_cls')
            actual_cls = importstr(actual_str)

            if hasattr(actual_cls, 'fromJson'):
                return actual_cls.fromJson(json_dict)

        return json_dict

    @staticmethod
    def loads(*args, **kwargs):
        kwargs.setdefault('object_hook', Jsonable._object_hook)
        return json.loads(*args, **kwargs)

    @staticmethod
    def _default(obj):
        if isinstance(obj, Jsonable):
            return obj.toJson()

        raise TypeError("{!r} is not Jsonable.".format(type(obj)))

    @staticmethod
    def dumps(*args, **kwargs):
        kwargs.setdefault('sort_keys', True)
        kwargs.setdefault('default', Jsonable._default)

        return json.dumps(*args, **kwargs)

    @classmethod
    def fromJson(cls, json_dict, **kwargs):
        init_kwargs = {}
        init_kwargs.update(json_dict)
        init_kwargs.update(kwargs)

        return cls(**init_kwargs)

    def toJson(self, **kwargs):
        cls = type(self)
        json_dict = {'_cls': '{}:{}'.format(cls.__module__, cls.__name__)}

        for k, v in self.__dict__.items():
            if (self.jsonAttr_set and k not in self.jsonAttr_set) or (self.jsonSkip_set and k in self.jsonSkip_set):
                pass
            else:
                json_dict[k] = v

        return json_dict

_fancyRepr_depth = 0
class FancyRepr(object):
    _repr_max_depth = 2
    _repr_keys = set()

    def __repr__(self):
        global _fancyRepr_depth

        r = super().__repr__()
        r = re.sub(r'\<([a-z_]+\.)+', '<', r)
        r = r.replace(' object at', '')

        _fancyRepr_depth += 1
        try:
            if _fancyRepr_depth < 2:
                attr_list = sorted(self.__dict__.items())
                join_str = ', ' if len(attr_list) < 30 else ('\n' + '    ' * _fancyRepr_depth)
                extra_str = join_str.join(['{}:{!r}'.format(k, v) for k, v in attr_list if not self._repr_keys or k in self._repr_keys])
                r = r.replace('>', join_str + '{}>'.format(extra_str))
        finally:
            _fancyRepr_depth -= 1

        return r
