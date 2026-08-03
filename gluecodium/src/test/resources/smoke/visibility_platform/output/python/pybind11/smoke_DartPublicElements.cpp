

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
#include "smoke/DartPublicElements.h"

using DartPublicElements = ::smoke::DartPublicElements;



void register_smoke_DartPublicElements(py::module_& module) {
auto cls_DartPublicElements = py::class_<DartPublicElements>(module, "smoke_DartPublicElements")
        .def(py::init<>())
        .def(py::init([]() {
            return DartPublicElements(::std::string{});
        }))
        ;


}
