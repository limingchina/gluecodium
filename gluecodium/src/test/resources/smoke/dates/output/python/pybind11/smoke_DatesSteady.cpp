

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DatesSteady.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DatesSteady = ::gluecodium::smoke::DatesSteady;

void register_DatesSteady(py::module_& module) {
    py::class_<DatesSteady, std::shared_ptr<DatesSteady>>(module, "DatesSteady")
        .def("date_method", &DatesSteady::date_method, py::arg("input"))
        .def("nullable_date_method", &DatesSteady::nullable_date_method, py::arg("input"))
        .def("date_list_method", &DatesSteady::date_list_method, py::arg("input"))
        ;
}

