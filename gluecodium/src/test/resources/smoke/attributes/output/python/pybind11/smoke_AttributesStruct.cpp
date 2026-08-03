

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
#include "smoke/AttributesStruct.h"
#include "string"

using AttributesStruct = ::smoke::AttributesStruct;



void register_smoke_AttributesStruct(py::module_& module) {
auto cls_AttributesStruct = py::class_<AttributesStruct>(module, "smoke_AttributesStruct")
        .def_readwrite("field", &AttributesStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        .def("very_fun", &AttributesStruct::very_fun, py::arg("param"))
        ;


}
