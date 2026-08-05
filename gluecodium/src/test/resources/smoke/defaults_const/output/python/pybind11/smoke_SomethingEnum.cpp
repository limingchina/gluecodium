

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
#include "smoke/SomethingEnum.h"

using SomethingEnum = ::smoke::SomethingEnum;



void register_smoke_SomethingEnum(py::module_& module) {
auto cls_SomethingEnum = py::enum_<SomethingEnum>(module, "smoke_SomethingEnum")
        .value("REALLY_FIRST", SomethingEnum::REALLY_FIRST)
        .value("EXPLICIT", SomethingEnum::EXPLICIT)
        .value("LAST", SomethingEnum::LAST)
        ;


}
