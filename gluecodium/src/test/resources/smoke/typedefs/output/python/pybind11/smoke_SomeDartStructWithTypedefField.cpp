

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/GlobalListTypeDef.h"
#include "smoke/SomeDartStructWithTypedefField.h"

void register_SomeDartStructWithTypedefField(py::module_& module) {
    py::class_<SomeDartStructWithTypedefField>(module, "SomeDartStructWithTypedefField")
        .def_readwrite("some_field", &SomeDartStructWithTypedefField::some_field)
        ;
}

