

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalElements.h"
#include "string"

void register_DartInternalElements(py::module_& module) {
    py::class_<DartInternalElements>(module, "DartInternalElements")
        .def_readwrite("string_field", &DartInternalElements::string_field)
        .def("foo", &DartInternalElements::foo)
        ;
}

