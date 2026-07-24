

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SomeInternalEnum.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeInternalEnum = ::smoke::SomeInternalEnum;

void register_smoke_SomeInternalEnum(py::module_& module) {
    py::enum_<SomeInternalEnum>(module, "SomeInternalEnum")
        .value("ONE", SomeInternalEnum::ONE)
        .value("TWO", SomeInternalEnum::TWO)
        .value("THREE", SomeInternalEnum::THREE)
        .value("SINGLE", SomeInternalEnum::SINGLE)
        ;
}

