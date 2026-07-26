

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
#include "gluecodium/VectorHash.h"
#include "package/Types.h"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Types = ::package::Types;

void register_package_Types(py::module_& module) {
    py::class_<Types>(module, "package_Types")
        .def(py::init<>())
        ;
}

