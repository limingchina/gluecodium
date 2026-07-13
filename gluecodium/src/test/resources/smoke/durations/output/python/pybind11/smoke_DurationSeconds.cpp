

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/DurationSeconds.h"
#include "chrono"
#include "optional"

void register_DurationSeconds(py::module_& module) {
    py::class_<DurationSeconds>(module, "DurationSeconds")
        .def("duration_function", &DurationSeconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationSeconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", &DurationSeconds::get_duration_property)
        ;
}

