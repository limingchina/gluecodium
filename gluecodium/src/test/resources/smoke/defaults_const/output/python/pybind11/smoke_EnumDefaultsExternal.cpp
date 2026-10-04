

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
#include "foo/AlienEnum1.h"
#include "foo/AlienEnum2.h"
#include "foo/AlienEnum3.h"
#include "gluecodium/Optional.h"
#include "smoke/EnumDefaultsExternal.h"
#include "smoke/EnumWrapper.h"

using EnumDefaultsExternal = ::smoke::EnumDefaultsExternal;
using SimpleEnum = ::smoke::EnumDefaultsExternal::SimpleEnum;
using NullableEnum = ::smoke::EnumDefaultsExternal::NullableEnum;
using AliasEnum = ::smoke::EnumDefaultsExternal::AliasEnum;
using WrappedEnum = ::smoke::EnumDefaultsExternal::WrappedEnum;



void register_smoke_EnumDefaultsExternal(py::module_& module) {
auto cls_EnumDefaultsExternal = py::class_<EnumDefaultsExternal, std::shared_ptr<EnumDefaultsExternal>>(module, "smoke_EnumDefaultsExternal")
        .def("__gluecodium_id__", [](const EnumDefaultsExternal& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_EnumDefaultsExternalSimpleEnum = py::class_<SimpleEnum>(cls_EnumDefaultsExternal, "SimpleEnum")
        .def_property("enum_field", [](const SimpleEnum& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](SimpleEnum& self, const foo::AlienEnum1 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<foo::AlienEnum1>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsExternalNullableEnum = py::class_<NullableEnum>(cls_EnumDefaultsExternal, "NullableEnum")
        .def_property("enum_field1", [](const NullableEnum& self) -> decltype(auto) {
            return
                (self.enum_field1)
            ;
        }, [](NullableEnum& self, const ::gluecodium::optional< foo::AlienEnum2 >& value) {

                self.enum_field1 = value;

        })
        .def_property("enum_field2", [](const NullableEnum& self) -> decltype(auto) {
            return
                (self.enum_field2)
            ;
        }, [](NullableEnum& self, const ::gluecodium::optional< foo::AlienEnum2 >& value) {

                self.enum_field2 = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< foo::AlienEnum2 >, ::gluecodium::optional< foo::AlienEnum2 >>(), py::arg("enum_field1"), py::arg("enum_field2"))
        ;

auto cls_EnumDefaultsExternalAliasEnum = py::class_<AliasEnum>(cls_EnumDefaultsExternal, "AliasEnum")
        .def_property("enum_field", [](const AliasEnum& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](AliasEnum& self, const foo::AlienEnum3 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<foo::AlienEnum3>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsExternalWrappedEnum = py::class_<WrappedEnum>(cls_EnumDefaultsExternal, "WrappedEnum")
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
