

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicElements.h"

void register_DartPublicElements(py::module_& module) {
    py::class_<DartPublicElements>(module, "DartPublicElements")
        .def_readwrite("string_field", &DartPublicElements::string_field)
        .def("foo", &DartPublicElements::foo)
        ;
}

