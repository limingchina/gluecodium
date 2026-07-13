

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SomethingEnum.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomethingEnum = ::gluecodium::smoke::SomethingEnum;

void register_SomethingEnum(py::module_& module) {
    py::enum_<SomethingEnum>(module, "SomethingEnum")
        .value("REALLY_FIRST", SomethingEnum::REALLY_FIRST)
        .value("EXPLICIT", SomethingEnum::EXPLICIT)
        .value("LAST", SomethingEnum::LAST)
        ;
}

