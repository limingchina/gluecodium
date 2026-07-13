

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaInternalProperty.h"
#include "optional"
#include "string"

void register_JavaInternalProperty(py::module_& module) {
    py::class_<JavaInternalProperty>(module, "JavaInternalProperty")
        .def_property("app_context", &JavaInternalProperty::get_app_context)
        ;
}

