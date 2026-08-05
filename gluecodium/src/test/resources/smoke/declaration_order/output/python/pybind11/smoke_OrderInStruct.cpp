

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
#include "smoke/OrderInStruct.h"
#include "string"

using OrderInStruct = ::smoke::OrderInStruct;
using NestedStruct = ::smoke::OrderInStruct::NestedStruct;
using SomeEnum = ::smoke::OrderInStruct::SomeEnum;



void register_smoke_OrderInStruct(py::module_& module) {
auto cls_OrderInStruct = py::class_<OrderInStruct>(module, "smoke_OrderInStruct")
        .def_readwrite("struct_field", &OrderInStruct::struct_field)
        .def_readwrite("enum_field", &OrderInStruct::enum_field)
        .def(py::init<>())
        .def(py::init<::smoke::OrderInStruct::NestedStruct, ::smoke::OrderInStruct::SomeEnum>(), py::arg("struct_field"), py::arg("enum_field"))
        ;

auto cls_OrderInStructNestedStruct = py::class_<NestedStruct>(cls_OrderInStruct, "NestedStruct")
        .def_readwrite("some_field", &NestedStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_OrderInStructSomeEnum = py::enum_<SomeEnum>(cls_OrderInStruct, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
