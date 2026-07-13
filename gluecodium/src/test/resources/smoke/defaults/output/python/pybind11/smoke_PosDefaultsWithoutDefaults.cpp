

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PosDefaultsWithoutDefaults.h"
#include "string"

void register_PosDefaultsWithoutDefaults(py::module_& module) {
    py::class_<PosDefaultsWithoutDefaults>(module, "PosDefaultsWithoutDefaults")
        .def_readwrite("string_field", &PosDefaultsWithoutDefaults::string_field)
        ;
}

