

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ExcludedCommentsOnly.h"
#include "cstdint"
#include "functional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExcludedCommentsOnly = ::gluecodium::smoke::ExcludedCommentsOnly;

void register_ExcludedCommentsOnly(py::module_& module) {
    py::class_<ExcludedCommentsOnly>(module, "ExcludedCommentsOnly")
        .def("some_method_with_all_comments", &ExcludedCommentsOnly::some_method_with_all_comments, py::arg("input_parameter"))
        .def("some_method_without_return_type_or_input_parameters", &ExcludedCommentsOnly::some_method_without_return_type_or_input_parameters)
        .def_property("is_some_property", py::overload_cast<>(&ExcludedCommentsOnly::is_some_property, py::const_), py::overload_cast<const bool>(&ExcludedCommentsOnly::set_some_property))
        ;
}

