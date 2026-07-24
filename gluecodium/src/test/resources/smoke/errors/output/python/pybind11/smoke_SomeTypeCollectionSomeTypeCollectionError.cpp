

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SomeTypeCollection.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeTypeCollectionError = ::smoke::SomeTypeCollection::SomeTypeCollectionError;

void register_smoke_SomeTypeCollectionSomeTypeCollectionError(py::module_& module) {
    py::enum_<SomeTypeCollectionError>(module, "SomeTypeCollectionSomeTypeCollectionError")
        .value("ERROR_A", SomeTypeCollectionError::ERROR_A)
        .value("ERROR_B", SomeTypeCollectionError::ERROR_B)
        ;
}

