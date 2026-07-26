

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
#include "dont/smoke/DontSmokeEnum.h"
#include "smoke/SkippedFunctionClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkippedFunctionClass = ::smoke::SkippedFunctionClass;


void register_smoke_SkippedFunctionClass(py::module_& module) {
    py::class_<SkippedFunctionClass, std::shared_ptr<SkippedFunctionClass>>(module, "smoke_SkippedFunctionClass")
        .def("do_foo", &SkippedFunctionClass::do_foo, py::arg("input"))
        ;
}

