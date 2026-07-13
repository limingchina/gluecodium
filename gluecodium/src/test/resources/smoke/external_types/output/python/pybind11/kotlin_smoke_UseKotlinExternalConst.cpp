

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/UseKotlinExternalConst.h"
#include "string"

void register_UseKotlinExternalConst(py::module_& module) {
    py::class_<UseKotlinExternalConst>(module, "UseKotlinExternalConst")
        .def_readwrite("string_field", &UseKotlinExternalConst::string_field)
        ;
}

