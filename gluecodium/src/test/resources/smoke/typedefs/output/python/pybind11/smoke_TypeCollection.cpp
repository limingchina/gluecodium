

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
#include "smoke/TypeCollection.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using TypeCollection = ::smoke::TypeCollection;

void register_smoke_TypeCollection(py::module_& module) {
    py::class_<TypeCollection>(module, "smoke_TypeCollection")
        .def(py::init<>())
        ;
}

