

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
#include "smoke/FieldConstructorsSkipTag.h"
#include "string"

using FieldConstructorsSkipTag = ::smoke::FieldConstructorsSkipTag;



void register_smoke_FieldConstructorsSkipTag(py::module_& module) {
auto cls_FieldConstructorsSkipTag = py::class_<FieldConstructorsSkipTag>(module, "smoke_FieldConstructorsSkipTag")
        .def_readwrite("field1", &FieldConstructorsSkipTag::field1)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field1"))
        ;


}
