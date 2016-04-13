from droidblue.dice import AttackDicePool, DefenseDicePool

import pytest

@pytest.fixture
def atk1():
    return AttackDicePool(1)
@pytest.fixture
def atk2():
    return AttackDicePool(2)
@pytest.fixture
def atk3():
    return AttackDicePool(3)

@pytest.fixture
def dfn1():
    return DefenseDicePool(1)
@pytest.fixture
def dfn2():
    return DefenseDicePool(2)
@pytest.fixture
def dfn3():
    return DefenseDicePool(3)

def test_atk1_probs(atk1):
    random_list = atk1.getRollRandomList()
    result_dict = {pool.rolled_faces: prob_frac for (prob_frac, pool) in random_list}
    golden_dict = {
        'C': 1/8.,
        'H': 3/8.,
        'f': 2/8.,
        'x': 2/8.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

def test_atk2_probs(atk2):
    random_list = atk2.getRollRandomList()
    result_dict = {pool.rolled_faces: prob_frac for (prob_frac, pool) in random_list}
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

def test_dfn1_probs(dfn1):
    random_list = dfn1.getRollRandomList()
    result_dict = {pool.rolled_faces: prob_frac for (prob_frac, pool) in random_list}
    golden_dict = {
        'E': 3/8.,
        'f': 2/8.,
        'x': 3/8.,
    }
    assert result_dict == golden_dict
    assert sum(result_dict.values()) == 1.0

def test_dfn2_probs(dfn2):
    random_list = dfn2.getRollRandomList()
    result_dict = {pool.rolled_faces: prob_frac for (prob_frac, pool) in random_list}
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

def test_reroll():
    hf_pool = AttackDicePool(0, rolled_faces='Hf')
    choice_dict = hf_pool.getRerollChoiceDict('f', 1)

    assert choice_dict[''].rolled_faces == 'Hf'
    assert choice_dict[''].removed_faces == ''
    assert choice_dict[''].rerolled_faces == None
    assert choice_dict[''].count == 0
    assert len(choice_dict[''].getRollRandomList()) == 1

    assert choice_dict['f'].rolled_faces == 'H'
    assert choice_dict['f'].removed_faces == 'f'
    assert choice_dict['f'].rerolled_faces == None
    assert choice_dict['f'].count == 1
    assert len(choice_dict['f'].getRollRandomList()) == 4

    assert choice_dict.keys() == []


