from ..util import Jsonable

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class JsonableTest(Jsonable):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_jsonable():
    j = {
        'l': [1, 2, 3],
        'jt': JsonableTest()
    }

    s = Jsonable.dumps(j, indent=4)
    log.debug(s)
    l = Jsonable.loads(s)

    assert isinstance(l['jt'], JsonableTest)

def test_jsonable_recursive():
    j = {
        'l': [1, 2, 3],
        'jt': JsonableTest(
            jt2=JsonableTest(a='a'),
            r=[JsonableTest(b='b')],
        )
    }

    s = Jsonable.dumps(j, indent=4)
    log.debug(s)
    l = Jsonable.loads(s)

    assert isinstance(l['jt'], JsonableTest)
    assert isinstance(l['jt'].jt2, JsonableTest)
    assert isinstance(l['jt'].r[0], JsonableTest)
