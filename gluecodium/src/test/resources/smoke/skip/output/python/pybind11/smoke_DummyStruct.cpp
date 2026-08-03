

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
#include "smoke/DummyStruct.h"
#include "string"

using DummyStruct = ::smoke::DummyStruct;



void register_smoke_DummyStruct(py::module_& module) {
auto cls_DummyStruct = py::class_<DummyStruct>(module, "smoke_DummyStruct")
        .def_readwrite("string_field", &DummyStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
