

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaInternalPropertyRev.h"
#include "optional"
#include "string"

void register_JavaInternalPropertyRev(py::module_& module) {
    py::class_<JavaInternalPropertyRev>(module, "JavaInternalPropertyRev")
        .def_property("app_context", &JavaInternalPropertyRev::get_app_context)
        ;
}

