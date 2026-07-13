

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterStructWithFieldConstructor.h"

void register_OuterStructWithFieldConstructor(py::module_& module) {
    py::class_<OuterStructWithFieldConstructor>(module, "OuterStructWithFieldConstructor")
        .def_readwrite("outer_struct_field", &OuterStructWithFieldConstructor::outer_struct_field)
        ;
}

