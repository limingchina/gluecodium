

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
#include "smoke/Month.h"

using Month = ::smoke::Month;



void register_smoke_Month(py::module_& module) {
auto cls_Month = py::enum_<Month>(module, "smoke_Month")
        .value("JANUARY", Month::JANUARY)
        .value("FEBRUARY", Month::FEBRUARY)
        .value("MARCH", Month::MARCH)
        ;


}
