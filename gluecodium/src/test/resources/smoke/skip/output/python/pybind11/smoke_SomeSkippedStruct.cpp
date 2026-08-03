

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
#include "gluecodium/VectorHash.h"
#include "smoke/SomeSkippedEnum.h"
#include "smoke/SomeSkippedStruct.h"
#include "vector"

using SomeSkippedStruct = ::smoke::SomeSkippedStruct;



void register_smoke_SomeSkippedStruct(py::module_& module) {
auto cls_SomeSkippedStruct = py::class_<SomeSkippedStruct>(module, "smoke_SomeSkippedStruct")
        .def_readwrite("field", &SomeSkippedStruct::field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::SomeSkippedEnum >>(), py::arg("field"))
        .def("__eq__", [](const SomeSkippedStruct& lhs, const SomeSkippedStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const SomeSkippedStruct& self) { return gluecodium::hash<SomeSkippedStruct>{}(self); })
        ;


}
