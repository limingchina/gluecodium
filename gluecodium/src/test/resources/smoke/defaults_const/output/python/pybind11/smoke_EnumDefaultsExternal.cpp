

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
#include "smoke/EnumDefaultsExternal.h"
#include "smoke/EnumWrapper.h"
#include "optional"

using EnumDefaultsExternal = ::smoke::EnumDefaultsExternal;
using SimpleEnum = ::smoke::EnumDefaultsExternal::SimpleEnum;
using NullableEnum = ::smoke::EnumDefaultsExternal::NullableEnum;
using AliasEnum = ::smoke::EnumDefaultsExternal::AliasEnum;
using WrappedEnum = ::smoke::EnumDefaultsExternal::WrappedEnum;



void register_smoke_EnumDefaultsExternal(py::module_& module) {
auto cls_EnumDefaultsExternal = py::class_<EnumDefaultsExternal, std::shared_ptr<EnumDefaultsExternal>>(module, "smoke_EnumDefaultsExternal")
        .def("__gluecodium_id__", [](const EnumDefaultsExternal& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_EnumDefaultsExternalSimpleEnum = py::class_<SimpleEnum>(cls_EnumDefaultsExternal, "SimpleEnum")
        .def_readwrite("enum_field", &SimpleEnum::enum_field)
        .def(py::init<>())
        .def(py::init<foo::AlienEnum1>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsExternalNullableEnum = py::class_<NullableEnum>(cls_EnumDefaultsExternal, "NullableEnum")
        .def_readwrite("enum_field1", &NullableEnum::enum_field1)
        .def_readwrite("enum_field2", &NullableEnum::enum_field2)
        .def(py::init<>())
        .def(py::init<std::optional< foo::AlienEnum2 >, std::optional< foo::AlienEnum2 >>(), py::arg("enum_field1"), py::arg("enum_field2"))
        ;

auto cls_EnumDefaultsExternalAliasEnum = py::class_<AliasEnum>(cls_EnumDefaultsExternal, "AliasEnum")
        .def_readwrite("enum_field", &AliasEnum::enum_field)
        .def(py::init<>())
        .def(py::init<foo::AlienEnum3>(), py::arg("enum_field"))
        ;

auto cls_EnumDefaultsExternalWrappedEnum = py::class_<WrappedEnum>(cls_EnumDefaultsExternal, "WrappedEnum")
        .def_readwrite("struct_field", &WrappedEnum::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::EnumWrapper>(), py::arg("struct_field"))
        ;


}
