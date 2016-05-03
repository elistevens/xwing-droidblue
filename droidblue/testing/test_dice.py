from __future__ import division

from droidblue.core.dice import AttackDicePool
from droidblue.testing.fixtures import *


def test_atk1_pool_probs(atk1_pool):
    result_dict = atk1_pool.rollDice()
    golden_dict = {
        'C': 1/8.,
        'H': 3/8.,
        'f': 2/8.,
        'x': 2/8.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

    assert set(atk1_pool.cache) >= {0,1}

def test_atk2_pool_probs(atk2_pool):
    result_dict = atk2_pool.rollDice()
    golden_dict = {
        'CC':  1/64.,
        'CH':  6/64.,
        'Cf':  4/64.,
        'Cx':  4/64.,
        'HH':  9/64.,
        'Hf': 12/64.,
        'Hx': 12/64.,
        'ff':  4/64.,
        'fx':  8/64.,
        'xx':  4/64.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

    assert set(atk2_pool.cache) >= {0,1,2}

def test_dfn1_probs(dfn1):
    result_dict = dfn1.rollDice()
    golden_dict = {
        'E': 3/8.,
        'f': 2/8.,
        'x': 3/8.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

    assert set(dfn1.cache) >= {0,1}

def test_dfn2_probs(dfn2):
    result_dict = dfn2.rollDice()
    golden_dict = {
        'EE':  9/64.,
        'Ef': 12/64.,
        'Ex': 18/64.,
        'ff':  4/64.,
        'fx': 12/64.,
        'xx':  9/64.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

    assert set(dfn2.cache) >= {0,1,2}

def test_modify():
    hf_pool = AttackDicePool(0, rolled_faces='Hf')
    hf_pool.modifyFaces('f', 'H', 99)
    assert hf_pool.getResults() == 'HH'

def test_reroll():
    hf_pool = AttackDicePool(0, rolled_faces='Hf')
    assert hf_pool.getResults() == 'Hf'
    assert {'f', ''} == hf_pool.getRerollOptions('f', 1)

    hf_pool.flagForReroll('f')
    assert hf_pool.getResults() == 'H'

    result_dict = hf_pool.rollDice()
    golden_dict = {
        'C': 1/8.,
        'H': 3/8.,
        'f': 2/8.,
        'x': 2/8.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

    hf_pool.setReroll('x')
    assert hf_pool.getResults() == 'Hx'

