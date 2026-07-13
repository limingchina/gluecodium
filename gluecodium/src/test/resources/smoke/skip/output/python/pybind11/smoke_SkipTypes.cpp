

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/SkipTypes.h"
#include "string"
#include "vector"

void register_SkipTypes(py::module_& module) {
    py::class_<SkipTypes>(module, "SkipTypes")
        .def("use_list_in_dart", &SkipTypes::use_list_in_dart)
        ;
}

