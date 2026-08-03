

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
#include "smoke/SkipFieldConstructorsClash.h"
#include "string"

using SkipFieldConstructorsClash = ::smoke::SkipFieldConstructorsClash;



void register_smoke_SkipFieldConstructorsClash(py::module_& module) {
auto cls_SkipFieldConstructorsClash = py::class_<SkipFieldConstructorsClash>(module, "smoke_SkipFieldConstructorsClash")
        .def_readwrite("param", &SkipFieldConstructorsClash::param)
        .def(py::init<>())
        ;


}
