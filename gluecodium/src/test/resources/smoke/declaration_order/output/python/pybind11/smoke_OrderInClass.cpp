

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
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_OrderInClassMainStruct = py::class_<MainStruct>(cls_OrderInClass, "MainStruct")
        .def_readwrite("struct_field", &MainStruct::struct_field)
        .def_readwrite("type_def_field", &MainStruct::type_def_field)
        .def_readwrite("struct_array_field", &MainStruct::struct_array_field)
        .def_readwrite("map_field", &MainStruct::map_field)
        .def_readwrite("enum_field", &MainStruct::enum_field)
        .def(py::init<>())
        .def(py::init<::smoke::OrderInClass::NestedStruct, int32_t, ::std::vector< ::smoke::OrderInClass::NestedStruct >, ::std::unordered_map< int32_t, ::std::vector< ::smoke::OrderInClass::NestedStruct > >, ::smoke::OrderInClass::SomeEnum>(), py::arg("struct_field"), py::arg("type_def_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("enum_field"))
        ;

auto cls_OrderInClassNestedStruct = py::class_<NestedStruct>(cls_OrderInClass, "NestedStruct")
        .def_readwrite("some_field", &NestedStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_OrderInClassSomeEnum = py::enum_<SomeEnum>(cls_OrderInClass, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
