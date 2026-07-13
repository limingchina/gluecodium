

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterName.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterName = ::gluecodium::smoke::OuterName;

void register_OuterName(py::module_& module) {
    py::class_<OuterName, std::shared_ptr<OuterName>>(module, "OuterName")
        ;
}

