

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ExcludedComments.h"
#include "cstdint"
#include "functional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExcludedComments = ::smoke::ExcludedComments;


void register_smoke_ExcludedComments(py::module_& module) {
    py::class_<ExcludedComments, std::shared_ptr<ExcludedComments>>(module, "smoke_ExcludedComments")
        .def("some_method_with_all_comments", &ExcludedComments::some_method_with_all_comments, py::arg("input_parameter"))
        .def("some_method_without_return_type_or_input_parameters", &ExcludedComments::some_method_without_return_type_or_input_parameters)
        .def_property("is_some_property", py::overload_cast<>(&ExcludedComments::is_some_property, py::const_), py::overload_cast<const bool>(&ExcludedComments::set_some_property))
        ;
}

