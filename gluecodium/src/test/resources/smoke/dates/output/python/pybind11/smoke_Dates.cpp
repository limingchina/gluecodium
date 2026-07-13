

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/Dates.h"
#include "chrono"
#include "optional"
#include "unordered_set"

void register_Dates(py::module_& module) {
    py::class_<Dates>(module, "Dates")
        .def("date_method", &Dates::date_method, py::arg("input"))
        .def("nullable_date_method", &Dates::nullable_date_method, py::arg("input"))
        .def_property("date_property", &Dates::get_date_property)
        .def_property("date_set", &Dates::get_date_set)
        ;
}

