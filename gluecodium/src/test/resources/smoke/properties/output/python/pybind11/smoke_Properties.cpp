

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
#include "gluecodium/VectorHash.h"
#include "smoke/Properties.h"
#include "smoke/PropertiesInterface.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

using Properties = ::smoke::Properties;
using ExampleStruct = ::smoke::Properties::ExampleStruct;
using InternalErrorCode = ::smoke::Properties::InternalErrorCode;



void register_smoke_Properties(py::module_& module) {
auto cls_Properties = py::class_<Properties, std::shared_ptr<Properties>>(module, "smoke_Properties")
        .def("__gluecodium_id__", [](const Properties& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_property("built_in_type_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_built_in_type_property();
            });
        }, [](Properties& self, const uint32_t value) {
            gluecodium::python::call_native([&] {
                self.set_built_in_type_property(value);
            });
        })
        .def_property_readonly("readonly_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_readonly_property();
            });
        })
        .def_property("struct_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_struct_property();
            });
        }, [](Properties& self, const ::smoke::Properties::ExampleStruct& value) {
            gluecodium::python::call_native([&] {
                self.set_struct_property(value);
            });
        })
        .def_property("array_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_array_property();
            }));
        }, [](Properties& self, const ::std::vector< ::std::string >& value) {
            gluecodium::python::call_native([&] {
                self.set_array_property(value);
            });
        })
        .def_property("complex_type_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_complex_type_property();
            });
        }, [](Properties& self, const ::smoke::Properties::InternalErrorCode value) {
            gluecodium::python::call_native([&] {
                self.set_complex_type_property(value);
            });
        })
        .def_property("byte_buffer_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_byte_buffer_property();
            });
        }, [](Properties& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {
            gluecodium::python::call_native([&] {
                self.set_byte_buffer_property(value);
            });
        })
        .def_property("instance_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_instance_property();
            });
        }, [](Properties& self, const ::std::shared_ptr< ::smoke::PropertiesInterface >& value) {
            gluecodium::python::call_native([&] {
                self.set_instance_property(value);
            });
        })
        .def_property("is_boolean_property", [](const Properties& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_boolean_property();
            });
        }, [](Properties& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_boolean_property(value);
            });
        })
        .def_static("static_property", []() -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return Properties::get_static_property();
            });
        })
        .def_static("static_property_set", [](const ::std::string& value) {
            gluecodium::python::call_native([&] {
                Properties::set_static_property(value);
            });
        })
        .def_static("static_readonly_property", []() -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return Properties::get_static_readonly_property();
            });
        })
        ;

auto cls_PropertiesExampleStruct = py::class_<ExampleStruct>(cls_Properties, "ExampleStruct")
        .def_property("value", [](const ExampleStruct& self) -> decltype(auto) {
            return
                (self.value)
            ;
        }, [](ExampleStruct& self, const double value) {

                self.value = value;

        })
        .def(py::init<>())
        .def(py::init<double>(), py::arg("value"))
        ;

auto cls_PropertiesInternalErrorCode = py::enum_<InternalErrorCode>(cls_Properties, "InternalErrorCode")
        .value("ERROR_NONE", InternalErrorCode::ERROR_NONE)
        .value("ERROR_FATAL", InternalErrorCode::ERROR_FATAL)
        ;


}
