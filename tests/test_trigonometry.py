from data import trigonometry


def round_tuple(tuple: tuple):
    return (round(tuple[0]), round(tuple[1]))


def test_reference():
    result = round_tuple(trigonometry.get_reference(10, 5.4, 5.4))
    assert result == (5, 2)

    result = round_tuple(trigonometry.get_reference(10, 9.43, 5.4))
    assert result == (8, 5)

    result = round_tuple(trigonometry.get_reference(10, 10.63, 7.2))
    assert result == (8, 7)

    result = round_tuple(trigonometry.get_reference(10, 9.43, 9.43))
    assert result == (5, 8)

    result = round_tuple(trigonometry.get_reference(10, 8.48, 7.21))
    assert result == (6, 6)

    result = round_tuple(trigonometry.get_reference(10, 5.4, 9.43))
    assert result == (2, 5)

    result = round_tuple(trigonometry.get_reference(10, 7.28, 10.63))
    assert result == (2, 7)
