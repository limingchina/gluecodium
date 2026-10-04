

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
#include "fire/Enum1.h"
#include "fire/Enum2.h"
#include "fire/Enum3.h"
#include "gluecodium/Optional.h"
#include "smoke/EnumDefaults.h"
#include "smoke/EnumWrapper.h"

using EnumDefaults = ::smoke::EnumDefaults;
using SimpleEnum = ::smoke::EnumDefaults::SimpleEnum;
using NullableEnum = ::smoke::EnumDefaults::NullableEnum;
using AliasEnum = ::smoke::EnumDefaults::AliasEnum;
using WrappedEnum = ::smoke::EnumDefaults::WrappedEnum;



void register_smoke_EnumDefaults(py::module_& module) {
auto cls_EnumDefaults = py::class_<EnumDefaults, std::shared_ptr<EnumDefaults>>(module, "smoke_EnumDefaults")
        .def("__gluecodium_id__", [](const EnumDefaults& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_EnumDefaultsSimpleEnum = py::class_<SimpleEnum>(cls_EnumDefaults, "SimpleEnum")
        .def_property("enum_field", [](const SimpleEnum& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](SimpleEnum& self, const ::fire::Enum1 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<::fire::Enum1>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsNullableEnum = py::class_<NullableEnum>(cls_EnumDefaults, "NullableEnum")
        .def_property("enum_field1", [](const NullableEnum& self) -> decltype(auto) {
            return
                (self.enum_field1)
            ;
        }, [](NullableEnum& self, const ::gluecodium::optional< ::fire::Enum2 >& value) {

                self.enum_field1 = value;

        })
        .def_property("enum_field1", [](const NullableEnum& self) -> decltype(auto) {
            return
                (self.enum_field1)
            ;
        }, [](NullableEnum& self, const ::gluecodium::optional< ::fire::Enum2 >& value) {

                self.enum_field1 = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::fire::Enum2 >, ::gluecodium::optional< ::fire::Enum2 >>(), py::arg("enum_field1"), py::arg("enum_field1"))
        ;

auto cls_EnumDefaultsAliasEnum = py::class_<AliasEnum>(cls_EnumDefaults, "AliasEnum")
        .def_property("enum_field", [](const AliasEnum& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](AliasEnum& self, const ::fire::Enum3 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<::fire::Enum3>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsWrappedEnum = py::class_<WrappedEnum>(cls_EnumDefaults, "WrappedEnum")
        .def_property("struct_field", [](const WrappedEnum& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](WrappedEnum& self, const ::smoke::EnumWrapper& value) {

                self.struct_field = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::EnumWrapper>(), py::arg("struct_field"))
        ;


}
