

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
#include "smoke/OrderInStructWithFunctions.h"
#include "string"

using OrderInStructWithFunctions = ::smoke::OrderInStructWithFunctions;
using NestedStruct = ::smoke::OrderInStructWithFunctions::NestedStruct;
using SomeEnum = ::smoke::OrderInStructWithFunctions::SomeEnum;



void register_smoke_OrderInStructWithFunctions(py::module_& module) {
auto cls_OrderInStructWithFunctions = py::class_<OrderInStructWithFunctions>(module, "smoke_OrderInStructWithFunctions")
        .def_readwrite("some_field", &OrderInStructWithFunctions::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        .def("do_stuff", &OrderInStructWithFunctions::do_stuff, py::arg("struct_foo"))
        ;

auto cls_OrderInStructWithFunctionsNestedStruct = py::class_<NestedStruct>(cls_OrderInStructWithFunctions, "NestedStruct")
        .def_readwrite("some_field", &NestedStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_OrderInStructWithFunctionsSomeEnum = py::enum_<SomeEnum>(cls_OrderInStructWithFunctions, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
