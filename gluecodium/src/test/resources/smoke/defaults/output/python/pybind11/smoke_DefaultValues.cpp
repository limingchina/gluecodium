

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "cstdint"
#include "optional"
#include "string"
#include "vector"

void register_DefaultValues(py::module_& module) {
    py::class_<DefaultValues>(module, "DefaultValues")
        .def("process_struct_with_defaults", &DefaultValues::process_struct_with_defaults, py::arg("input"))
        ;
}

