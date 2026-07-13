

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaDeprecatedPosDefaultsCustom.h"
#include "cstdint"
#include "string"

void register_JavaDeprecatedPosDefaultsCustom(py::module_& module) {
    py::class_<JavaDeprecatedPosDefaultsCustom>(module, "JavaDeprecatedPosDefaultsCustom")
        .def_readwrite("first_init_field", &JavaDeprecatedPosDefaultsCustom::first_init_field)
        .def_readwrite("first_free_field", &JavaDeprecatedPosDefaultsCustom::first_free_field)
        .def("custom", &JavaDeprecatedPosDefaultsCustom::custom)
        ;
}

