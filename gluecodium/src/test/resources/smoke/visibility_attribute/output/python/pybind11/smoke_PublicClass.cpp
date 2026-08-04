

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/PublicClass.h"
#include "string"
#include "unordered_map"
#include "vector"

using PublicClass = ::smoke::PublicClass;
using InternalStruct = ::smoke::PublicClass::InternalStruct;
using PublicStruct = ::smoke::PublicClass::PublicStruct;
using PublicStructWithInternalDefaults = ::smoke::PublicClass::PublicStructWithInternalDefaults;
using InternalEnum = ::smoke::PublicClass::InternalEnum;



void register_smoke_PublicClass(py::module_& module) {
auto cls_PublicClass = py::class_<PublicClass, std::shared_ptr<PublicClass>>(module, "smoke_PublicClass")
        .def("__gluecodium_id__", [](const PublicClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("_internal_method", &PublicClass::internal_method, py::arg("input"))
        .def_property("__internal_struct_property", py::overload_cast<>(&PublicClass::get_internal_struct_property, py::const_), py::overload_cast<const ::smoke::PublicClass::InternalStruct&>(&PublicClass::set_internal_struct_property))
        ;

auto cls__PublicClassInternalStruct = py::class_<InternalStruct>(cls_PublicClass, "_InternalStruct")
        .def_readwrite("string_field", &InternalStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;

auto cls_PublicClassPublicStruct = py::class_<PublicStruct>(cls_PublicClass, "PublicStruct")
        .def_readwrite("_internal_field", &PublicStruct::internal_field)
        .def(py::init<>())
        .def(py::init([]() {
            return PublicStruct(::smoke::PublicClass::InternalStruct{});
        }))
        ;

auto cls_PublicClassPublicStructWithInternalDefaults = py::class_<PublicStructWithInternalDefaults>(cls_PublicClass, "PublicStructWithInternalDefaults")
        .def_readwrite("_internal_field", &PublicStructWithInternalDefaults::internal_field)
        .def_readwrite("public_field", &PublicStructWithInternalDefaults::public_field)
        .def(py::init<>())
        .def(py::init<float>(), py::arg("public_field"))
        .def(py::init([](const float& public_field) {
            return PublicStructWithInternalDefaults(::std::string{}, public_field);
        }), py::arg("public_field"))
        ;

auto cls__PublicClassInternalEnum = py::enum_<InternalEnum>(cls_PublicClass, "_InternalEnum")
        .value("FOO", InternalEnum::FOO)
        .value("BAR", InternalEnum::BAR)
        ;


}
