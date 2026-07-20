

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableIfEnabled.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableIfEnabled = ::smoke::EnableIfEnabled;


void register_EnableIfEnabled(py::module_& module) {
    py::class_<EnableIfEnabled, std::shared_ptr<EnableIfEnabled>>(module, "EnableIfEnabled")
        .def_static("enable_if_unquoted", &EnableIfEnabled::enable_if_unquoted)

        .def_static("enable_if_unquoted_list", &EnableIfEnabled::enable_if_unquoted_list)

        .def_static("enable_if_quoted", &EnableIfEnabled::enable_if_quoted)

        .def_static("enable_if_quoted_list", &EnableIfEnabled::enable_if_quoted_list)

        .def_static("enable_if_tagged", &EnableIfEnabled::enable_if_tagged)

        .def_static("enable_if_tagged_list", &EnableIfEnabled::enable_if_tagged_list)

        .def_static("enable_if_mixed_list", &EnableIfEnabled::enable_if_mixed_list)

        ;
}

