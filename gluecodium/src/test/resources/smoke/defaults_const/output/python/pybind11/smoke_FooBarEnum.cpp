

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FooBarEnum.h"

using FooBarEnum = ::smoke::FooBarEnum;



void register_smoke_FooBarEnum(py::module_& module) {
auto cls_FooBarEnum = py::enum_<FooBarEnum>(module, "smoke_FooBarEnum")
        .value("FOO", FooBarEnum::FOO)
        .value("BAR", FooBarEnum::BAR)
        .value("BAZ", FooBarEnum::BAZ)
        ;


}
