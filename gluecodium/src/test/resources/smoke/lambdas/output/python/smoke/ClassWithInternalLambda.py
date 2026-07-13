

from smoke.InternalNestedLambda import InternalNestedLambda

class ClassWithInternalLambda:
    """"""

    def __init__(self, native):
        self._native = native


    def invoke_internal_lambda(self, lambda: InternalNestedLambda, value: str) -> bool:
        """"""
        return self._native.invoke_internal_lambda(lambda, value)

