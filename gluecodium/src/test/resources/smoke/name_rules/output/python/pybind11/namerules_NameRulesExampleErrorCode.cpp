

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "namerules/NameRules.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExampleErrorCode = ::namerules::NameRules::ExampleErrorCode;

void register_NameRulesExampleErrorCode(py::module_& module) {
    py::enum_<ExampleErrorCode>(module, "NameRulesExampleErrorCode")
        .value("NONE", ExampleErrorCode::NONE)
        .value("FATAL", ExampleErrorCode::FATAL)
        ;
}

