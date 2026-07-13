

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FreeEnum.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FreeEnum = ::gluecodium::smoke::FreeEnum;

void register_FreeEnum(py::module_& module) {
    py::enum_<FreeEnum>(module, "FreeEnum")
        .value("FOO", FreeEnum::FOO)
        .value("BAR", FreeEnum::BAR)
        ;
}

