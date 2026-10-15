

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
#include "smoke/DeclarationOrder.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "vector"

using DeclarationOrder = ::smoke::DeclarationOrder;
using MainStruct = ::smoke::DeclarationOrder::MainStruct;
using NestedStruct = ::smoke::DeclarationOrder::NestedStruct;
using SomeEnum = ::smoke::DeclarationOrder::SomeEnum;



void register_smoke_DeclarationOrder(py::module_& module) {
auto cls_DeclarationOrder = py::class_<DeclarationOrder>(module, "smoke_DeclarationOrder")
        .def(py::init<>())
        ;

auto cls_DeclarationOrderMainStruct = py::class_<MainStruct>(cls_DeclarationOrder, "MainStruct")
        .def_property("struct_field", [](const MainStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](MainStruct& self, const ::smoke::DeclarationOrder::NestedStruct& value) {

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
        }, [](MainStruct& self, const ::std::vector< ::smoke::DeclarationOrder::NestedStruct >& value) {

                self.struct_array_field = value;

        })
        .def_property("map_field", [](const MainStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](MainStruct& self, const ::std::unordered_map< int32_t, ::std::vector< ::smoke::DeclarationOrder::NestedStruct > >& value) {

                self.map_field = value;

        })
        .def_property("enum_field", [](const MainStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](MainStruct& self, const ::smoke::DeclarationOrder::SomeEnum value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::DeclarationOrder::NestedStruct, int32_t, ::std::vector< ::smoke::DeclarationOrder::NestedStruct >, ::std::unordered_map< int32_t, ::std::vector< ::smoke::DeclarationOrder::NestedStruct > >, ::smoke::DeclarationOrder::SomeEnum>(), py::arg("struct_field"), py::arg("type_def_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("enum_field"))
        ;

auto cls_DeclarationOrderNestedStruct = py::class_<NestedStruct>(cls_DeclarationOrder, "NestedStruct")
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

auto cls_DeclarationOrderSomeEnum = py::enum_<SomeEnum>(cls_DeclarationOrder, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
