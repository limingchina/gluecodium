

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
#include "root/space/smoke/BasicTypes.h"
#include "string"

using BasicTypes = ::root::space::smoke::BasicTypes;
using SomeStruct = ::root::space::smoke::BasicTypes::SomeStruct;



void register_smoke_BasicTypes(py::module_& module) {
auto cls_BasicTypes = py::class_<BasicTypes>(module, "smoke_BasicTypes")
        .def(py::init<>())
        ;

auto cls_BasicTypesSomeStruct = py::class_<SomeStruct>(cls_BasicTypes, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;


}
