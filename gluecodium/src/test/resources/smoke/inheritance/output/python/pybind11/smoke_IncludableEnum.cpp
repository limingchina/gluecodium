

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
#include "smoke/IncludableEnum.h"

using IncludableEnum = ::smoke::IncludableEnum;



void register_smoke_IncludableEnum(py::module_& module) {
auto cls_IncludableEnum = py::enum_<IncludableEnum>(module, "smoke_IncludableEnum")
        .value("FOO", IncludableEnum::FOO)
        ;


}
