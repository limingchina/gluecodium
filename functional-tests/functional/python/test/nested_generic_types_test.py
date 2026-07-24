from test.NestedGenericTypes import NestedGenericTypes


class TestNestedGenericTypes:
    def test_list_of_lists(self):
        value = [[1, 2], [3, 4]]

        assert NestedGenericTypes.method_with_list_of_lists(value) == value

    def test_map_of_maps(self):
        value = {1: {2: True, 3: False}, 4: {5: True}}

        assert NestedGenericTypes.method_with_map_of_maps(value) == {
            frozenset({(2, True), (3, False)}): 1,
            frozenset({(5, True)}): 4,
        }

    def test_set_of_sets(self):
        value = {frozenset({1, 2}), frozenset({3})}

        assert NestedGenericTypes.method_with_set_of_sets(value) == value

    def test_list_and_map(self):
        value = [{1: True, 2: False}, {1: True, 3: True}]

        assert NestedGenericTypes.method_with_list_and_map(value) == {
            1: [1, 1],
            2: [0],
            3: [1],
        }

    def test_list_and_set(self):
        value = [{1, 2}, {2, 3}]

        result = NestedGenericTypes.method_with_list_and_set(value)

        assert {frozenset(item) for item in result} == {
            frozenset({1, 2}),
            frozenset({2, 3}),
        }

    def test_map_and_set(self):
        value = {10: {1, 2}, 20: {2, 3}}

        result = NestedGenericTypes.method_with_map_and_set(value)

        assert {frozenset(item) for item in result} == {
            frozenset({(1, True), (2, True)}),
            frozenset({(2, True), (3, True)}),
        }

    def test_map_generic_keys(self):
        value = {frozenset({1, 2}): True, frozenset({3}): False}

        result = NestedGenericTypes.method_with_map_generic_keys(value)

        assert {frozenset(key): item for key, item in result.items()} == {
            frozenset({1, 2}): True,
            frozenset({3}): False,
        }