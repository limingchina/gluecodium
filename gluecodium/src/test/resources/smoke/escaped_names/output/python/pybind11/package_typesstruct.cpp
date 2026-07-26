

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
#include "package/Types.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Struct = ::package::Types::Struct;

void register_package_typesstruct(py::module_& module) {
    py::class_<Struct>(module, "package_typesstruct")
        .def_readwrite("null", &Struct::null)
        .def(py::init<>())
        .def(py::init<::package::Types::Enum>(), py::arg("null"))
        ;
}

