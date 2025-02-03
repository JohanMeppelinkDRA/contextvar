import pytest

from contextvar import ContextVar, Context


def test_use_contextvar():
    new_var = ContextVar("NEW_VAR", default_value=1)
    assert new_var * 2 == 2
    assert new_var / 2 == 0.5
    assert new_var + 2 == 3
    assert new_var - 2 == -1
    assert str(new_var) == "1"
    assert new_var == 1
    assert new_var < 1.1
    assert new_var <= 1
    assert new_var > 0.9
    assert new_var >= 1

    # check we cannot create the same contextvar again
    with pytest.raises(AssertionError):
        ContextVar("NEW_VAR", default_value=2)


def test_use_contetvar_iterable():
    test_set_var = ContextVar("TEST_SET_VAR", default_value={1, 2, 3})
    assert test_set_var == {1, 2, 3}
    assert 1 in test_set_var
    assert 4 not in test_set_var
    assert len(test_set_var) == 3

    test_dict_var = ContextVar("TEST_DICT_VAR", default_value={"a": 1, "b": 2, "c": 3})
    assert test_dict_var == {"a": 1, "b": 2, "c": 3}
    assert test_dict_var["a"] == 1
    # check we cannot overwrite the contextvars items
    with pytest.raises(TypeError):
        test_dict_var["a"] = 2  # type: ignore

    test_list_var = ContextVar("TEST_LIST_VAR", default_value=[1, 2, 3])
    # check we can iterate over the contextvar
    for i, item in enumerate(test_list_var):
        assert item == i + 1
    assert [i for i in test_list_var] == [1, 2, 3]


def test_use_context():
    var = ContextVar("VAR", default_value=0.5)
    assert var == 0.5

    # by using the context we can change the value of the context variable
    with Context(VAR=20.5):
        assert var == 20.5

    # show all context variables are reset
    assert var == 0.5
    # add a new context variable
    ContextVar("NEW_VAR2", default_value=-1)
    # get all context variables
    all_vars = Context.get_all()
    assert all_vars["VAR"] == 0.5
    assert all_vars["NEW_VAR2"] == -1
