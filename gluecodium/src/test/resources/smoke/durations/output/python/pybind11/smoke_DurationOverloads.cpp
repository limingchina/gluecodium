

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/DurationOverloads.h"
#include "chrono"
#include "string"

void register_DurationOverloads(py::module_& module) {
    py::class_<DurationOverloads>(module, "DurationOverloads")
        .def("duration_function", &DurationOverloads::duration_function, py::arg("input"))
        .def("duration_function", &DurationOverloads::duration_function, py::arg("input"))
        ;
}

