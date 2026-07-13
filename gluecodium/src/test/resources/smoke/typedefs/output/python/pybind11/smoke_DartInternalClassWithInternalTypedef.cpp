

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalClassWithInternalTypedef.h"

void register_DartInternalClassWithInternalTypedef(py::module_& module) {
    py::class_<DartInternalClassWithInternalTypedef>(module, "DartInternalClassWithInternalTypedef")
        .def_property("numbers", &DartInternalClassWithInternalTypedef::get_numbers)
        .def_property("labels", &DartInternalClassWithInternalTypedef::get_labels)
        ;
}

