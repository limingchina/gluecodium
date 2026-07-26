

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
#include "smoke/OuterStruct.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerEnum = ::smoke::OuterStruct::InnerEnum;

void register_smoke_OuterStructInnerEnum(py::module_& module) {
    py::enum_<InnerEnum>(module, "smoke_OuterStructInnerEnum")
        .value("FOO", InnerEnum::FOO)
        .value("BAR", InnerEnum::BAR)
        ;
}

