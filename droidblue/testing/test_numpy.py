# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import pytest
import numpy as np


def test_writeable():
    a = np.zeros((2,2), np.int8)
    a[1,1] = 1
    a.flags.writeable = False

    with pytest.raises(ValueError):
        a[1,1] = 2

    a.flags.writeable = True

    a[0,0] = 3
