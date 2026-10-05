

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
#include "VectorHash.h"
#include "namerules/NameRules.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

using NameRules = ::namerules::NameRules;
using ExampleStruct = ::namerules::NameRules::ExampleStruct;
using ExampleErrorCode = ::namerules::NameRules::ExampleErrorCode;



void register_namerules_NameRules(py::module_& module) {
auto cls_NameRules = py::class_<NameRules, std::shared_ptr<NameRules>>(module, "namerules_NameRules")
        .def("__gluecodium_id__", [](const NameRules& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("create", &NameRules::create, py::call_guard<py::gil_scoped_release>())
        .def("some_method", &NameRules::someMethod, py::arg("some_argument"), py::call_guard<py::gil_scoped_release>())
        .def_property("int_property", [](const NameRules& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.retrieve_int_property();
            });
        }, [](NameRules& self, const uint32_t value) {
            gluecodium::python::call_native([&] {
                self.STORE_INT_PROPERTY_NOW(value);
            });
        })
        .def_property("is_boolean_property", [](const NameRules& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.really_boolean_property();
            });
        }, [](NameRules& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.STORE_BOOLEAN_PROPERTY_NOW(value);
            });
        })
        .def_property("struct_property", [](const NameRules& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.retrieve_struct_property();
            });
        }, [](NameRules& self, const ::namerules::NameRules::ExampleStruct& value) {
            gluecodium::python::call_native([&] {
                self.STORE_STRUCT_PROPERTY_NOW(value);
            });
        })
        ;

auto cls_NameRulesExampleStruct = py::class_<ExampleStruct>(cls_NameRules, "ExampleStruct")
        .def_property("value", [](const ExampleStruct& self) -> decltype(auto) {
            return
                (self.m_value)
            ;
        }, [](ExampleStruct& self, const double value) {

                self.m_value = value;

        })
        .def_property("int_value", [](const ExampleStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.m_int_value)
            );
        }, [](ExampleStruct& self, const ::std::vector< int64_t >& value) {

                self.m_int_value = value;

        })
        .def(py::init<>())
        .def(py::init<double, ::std::vector< int64_t >>(), py::arg("value"), py::arg("int_value"))
        ;

auto cls_NameRulesExampleErrorCode = py::enum_<ExampleErrorCode>(cls_NameRules, "ExampleErrorCode")
        .value("NONE", ExampleErrorCode::NONE)
        .value("FATAL", ExampleErrorCode::FATAL)
        ;

    static py::exception<::std::error_code> exc_ExampleError(cls_NameRules, "ExampleError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_ExampleError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_ExampleError.ptr());


}
