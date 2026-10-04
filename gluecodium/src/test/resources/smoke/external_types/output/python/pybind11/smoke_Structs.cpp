

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "gluecodium/VectorHash.h"
#include "non/Sense.h"
#include "smoke/Structs.h"
#include "cstdint"
#include "string"
#include "vector"

using Structs = ::smoke::Structs;
using ExternalStruct = ::smoke::Structs::ExternalStruct;



void register_smoke_Structs(py::module_& module) {
auto cls_Structs = py::class_<Structs, std::shared_ptr<Structs>>(module, "smoke_Structs")
        .def("__gluecodium_id__", [](const Structs& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("get_external_struct", &Structs::get_external_struct)
        .def_static("get_another_external_struct", &Structs::get_another_external_struct)
        ;

auto cls_StructsExternalStruct = py::class_<ExternalStruct>(cls_Structs, "ExternalStruct")
        .def_readwrite("string_field", &ExternalStruct::stringField)
        .def_property("external_string_field", [](const ExternalStruct& self) {
            return self.get_some_string();
        }, [](ExternalStruct& self, const ::std::string& value) {
            self.set_some_string(value);
        })
        .def_property("external_array_field", [](const ExternalStruct& self) {
            return self.get_some_array();
        }, [](ExternalStruct& self, const ::std::vector< int8_t >& value) {
            self.set_some_array(value);
        })
        .def_property("external_struct_field", [](const ExternalStruct& self) {
            return self.get_some_struct();
        }, [](ExternalStruct& self, const ::fire::SomeVeryExternalStruct& value) {
            self.set_some_struct(value);
        })
        .def(py::init<>())
        .def(py::init([](const ::std::string& string_field, const ::std::string& external_string_field, const ::std::vector< int8_t >& external_array_field, const ::fire::SomeVeryExternalStruct& external_struct_field) {
            ExternalStruct result{};
            result.stringField = string_field;
            result.set_some_string(external_string_field);
            result.set_some_array(external_array_field);
            result.set_some_struct(external_struct_field);
            return result;
        }), py::arg("string_field"), py::arg("external_string_field"), py::arg("external_array_field"), py::arg("external_struct_field"))
        ;

auto cls_StructsAnotherExternalStruct = py::class_<::fire::SomeVeryExternalStruct>(cls_Structs, "AnotherExternalStruct")
        .def_readwrite("int_field", &::fire::SomeVeryExternalStruct::intField)
        .def(py::init<>())
        .def(py::init<int8_t>(), py::arg("int_field"))
        ;


}
