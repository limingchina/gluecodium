

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OrderInClass.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "vector"

using OrderInClass = ::smoke::OrderInClass;
using MainStruct = ::smoke::OrderInClass::MainStruct;
using NestedStruct = ::smoke::OrderInClass::NestedStruct;
using SomeEnum = ::smoke::OrderInClass::SomeEnum;



void register_smoke_OrderInClass(py::module_& module) {
auto cls_OrderInClass = py::class_<OrderInClass, std::shared_ptr<OrderInClass>>(module, "smoke_OrderInClass")
        .def("__gluecodium_id__", [](const OrderInClass& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_OrderInClassMainStruct = py::class_<MainStruct>(cls_OrderInClass, "MainStruct")
        .def_property("struct_field", [](const MainStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](MainStruct& self, const ::smoke::OrderInClass::NestedStruct& value) {

                self.struct_field = value;

        })
        .def_property("type_def_field", [](const MainStruct& self) -> decltype(auto) {
            return
                (self.type_def_field)
            ;
        }, [](MainStruct& self, const int32_t value) {

                self.type_def_field = value;

        })
        .def_property("struct_array_field", [](const MainStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.struct_array_field)
            );
        }, [](MainStruct& self, const ::std::vector< ::smoke::OrderInClass::NestedStruct >& value) {

                self.struct_array_field = value;

        })
        .def_property("map_field", [](const MainStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](MainStruct& self, const ::std::unordered_map< int32_t, ::std::vector< ::smoke::OrderInClass::NestedStruct > >& value) {

                self.map_field = value;

        })
        .def_property("enum_field", [](const MainStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](MainStruct& self, const ::smoke::OrderInClass::SomeEnum value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::OrderInClass::NestedStruct, int32_t, ::std::vector< ::smoke::OrderInClass::NestedStruct >, ::std::unordered_map< int32_t, ::std::vector< ::smoke::OrderInClass::NestedStruct > >, ::smoke::OrderInClass::SomeEnum>(), py::arg("struct_field"), py::arg("type_def_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("enum_field"))
        ;

auto cls_OrderInClassNestedStruct = py::class_<NestedStruct>(cls_OrderInClass, "NestedStruct")
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

auto cls_OrderInClassSomeEnum = py::enum_<SomeEnum>(cls_OrderInClass, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
