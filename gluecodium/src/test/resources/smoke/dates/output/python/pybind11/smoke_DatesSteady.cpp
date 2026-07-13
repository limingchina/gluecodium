

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DatesSteady.h"
#include "optional"

void register_DatesSteady(py::module_& module) {
    py::class_<DatesSteady>(module, "DatesSteady")
        .def("date_method", &DatesSteady::date_method, py::arg("input"))
        .def("nullable_date_method", &DatesSteady::nullable_date_method, py::arg("input"))
        .def("date_list_method", &DatesSteady::date_list_method, py::arg("input"))
        ;
}

