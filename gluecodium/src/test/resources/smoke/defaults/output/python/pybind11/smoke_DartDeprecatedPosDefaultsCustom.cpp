

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartDeprecatedPosDefaultsCustom.h"
#include "cstdint"
#include "string"

void register_DartDeprecatedPosDefaultsCustom(py::module_& module) {
    py::class_<DartDeprecatedPosDefaultsCustom>(module, "DartDeprecatedPosDefaultsCustom")
        .def_readwrite("int_field", &DartDeprecatedPosDefaultsCustom::int_field)
        .def_readwrite("string_field", &DartDeprecatedPosDefaultsCustom::string_field)
        .def("custom", &DartDeprecatedPosDefaultsCustom::custom)
        ;
}

