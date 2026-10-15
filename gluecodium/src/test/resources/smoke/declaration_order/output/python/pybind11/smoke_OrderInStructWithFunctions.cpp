

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
        .def_property("some_field", [](const OrderInStructWithFunctions& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](OrderInStructWithFunctions& self, const ::std::string& value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        .def("do_stuff", &OrderInStructWithFunctions::do_stuff, py::arg("struct_foo"), py::call_guard<py::gil_scoped_release>())
        ;

auto cls_OrderInStructWithFunctionsNestedStruct = py::class_<NestedStruct>(cls_OrderInStructWithFunctions, "NestedStruct")
        .def_property("some_field", [](const NestedStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](NestedStruct& self, const ::std::string& value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_OrderInStructWithFunctionsSomeEnum = py::enum_<SomeEnum>(cls_OrderInStructWithFunctions, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
