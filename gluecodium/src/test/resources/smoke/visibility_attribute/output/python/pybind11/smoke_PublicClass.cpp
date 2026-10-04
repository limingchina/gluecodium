

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
            return gluecodium::python::native_identity(self);
        })
        .def("_internal_method", &PublicClass::internal_method, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_property("_internal_struct_property", [](const PublicClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_internal_struct_property();
            });
        }, [](PublicClass& self, const ::smoke::PublicClass::InternalStruct& value) {
            gluecodium::python::call_native([&] {
                self.set_internal_struct_property(value);
            });
        })
        ;

auto cls__PublicClassInternalStruct = py::class_<InternalStruct>(cls_PublicClass, "_InternalStruct")
        .def_property("string_field", [](const InternalStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](InternalStruct& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;

auto cls_PublicClassPublicStruct = py::class_<PublicStruct>(cls_PublicClass, "PublicStruct")
        .def_property("_internal_field", [](const PublicStruct& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicStruct& self, const ::smoke::PublicClass::InternalStruct& value) {

                self.internal_field = value;

        })
        .def(py::init<>())
        .def(py::init([]() {
            return PublicStruct(::smoke::PublicClass::InternalStruct{});
        }))
        ;

auto cls_PublicClassPublicStructWithInternalDefaults = py::class_<PublicStructWithInternalDefaults>(cls_PublicClass, "PublicStructWithInternalDefaults")
        .def_property("_internal_field", [](const PublicStructWithInternalDefaults& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicStructWithInternalDefaults& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def_property("public_field", [](const PublicStructWithInternalDefaults& self) -> decltype(auto) {
            return
                (self.public_field)
            ;
        }, [](PublicStructWithInternalDefaults& self, const float value) {

                self.public_field = value;

        })
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
