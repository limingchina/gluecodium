

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/DurationMilliseconds.h"
#include "chrono"
#include "optional"

void register_DurationMilliseconds(py::module_& module) {
    py::class_<DurationMilliseconds>(module, "DurationMilliseconds")
        .def("duration_function", &DurationMilliseconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationMilliseconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", &DurationMilliseconds::get_duration_property)
        ;
}

