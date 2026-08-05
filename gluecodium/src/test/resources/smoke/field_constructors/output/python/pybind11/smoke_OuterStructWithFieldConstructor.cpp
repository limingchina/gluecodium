

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
#include "smoke/OuterStructWithFieldConstructor.h"

using OuterStructWithFieldConstructor = ::smoke::OuterStructWithFieldConstructor;
using InnerStructWithDefaults = ::smoke::OuterStructWithFieldConstructor::InnerStructWithDefaults;



void register_smoke_OuterStructWithFieldConstructor(py::module_& module) {
auto cls_OuterStructWithFieldConstructor = py::class_<OuterStructWithFieldConstructor>(module, "smoke_OuterStructWithFieldConstructor")
        .def_readwrite("outer_struct_field", &OuterStructWithFieldConstructor::outer_struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::OuterStructWithFieldConstructor::InnerStructWithDefaults>(), py::arg("outer_struct_field"))
        ;

auto cls_OuterStructWithFieldConstructorInnerStructWithDefaults = py::class_<InnerStructWithDefaults>(cls_OuterStructWithFieldConstructor, "InnerStructWithDefaults")
        .def_readwrite("inner_struct_field", &InnerStructWithDefaults::inner_struct_field)
        .def(py::init<>())
        .def(py::init<double>(), py::arg("inner_struct_field"))
        ;


}
