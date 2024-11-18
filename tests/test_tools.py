from ppga import tools


# generation tests
def test_repeat():
    """Test the repeated generation"""
    for i in range(1000):
        values = tools.gen_repetition([0, 1], i)
        assert len(values) == i


def test_permutation():
    """Test the permutation generation"""
    for i in range(1000):
        values = tools.gen_permutation([j for j in range(i)])
        assert len(values) == i
