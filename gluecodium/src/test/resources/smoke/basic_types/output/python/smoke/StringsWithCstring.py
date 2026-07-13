


class StringsWithCstring:
    """"""

    def __init__(self, native):
        self._native = native

    Method that takes a C string as input and returns an std::string it as output.
    def return_input_string_type(self, input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return self._native.return_input_string_type(input_string)

    Method that takes a C string as input and returns an std::string it as output.
    def return_input_string(self, input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return self._native.return_input_string(input_string)

