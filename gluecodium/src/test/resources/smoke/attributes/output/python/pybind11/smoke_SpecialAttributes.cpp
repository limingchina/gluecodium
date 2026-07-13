

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SpecialAttributes.h"

void register_SpecialAttributes(py::module_& module) {
    py::class_<SpecialAttributes>(module, "SpecialAttributes")
        .def("with_escaping", &SpecialAttributes::with_escaping)
        .def("with_line_break", &SpecialAttributes::with_line_break)
        ;
}

