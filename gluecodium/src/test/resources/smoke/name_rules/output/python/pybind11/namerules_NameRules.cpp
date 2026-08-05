

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
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &NameRules::create)
        .def("some_method", &NameRules::someMethod, py::arg("some_argument"))
        .def_property("int_property", py::overload_cast<>(&NameRules::retrieve_int_property, py::const_), py::overload_cast<const uint32_t>(&NameRules::STORE_INT_PROPERTY_NOW))
        .def_property("is_boolean_property", py::overload_cast<>(&NameRules::really_boolean_property, py::const_), py::overload_cast<const bool>(&NameRules::STORE_BOOLEAN_PROPERTY_NOW))
        .def_property("struct_property", py::overload_cast<>(&NameRules::retrieve_struct_property, py::const_), py::overload_cast<const ::namerules::NameRules::ExampleStruct&>(&NameRules::STORE_STRUCT_PROPERTY_NOW))
        ;

auto cls_NameRulesExampleStruct = py::class_<ExampleStruct>(cls_NameRules, "ExampleStruct")
        .def_readwrite("value", &ExampleStruct::m_value)
        .def_readwrite("int_value", &ExampleStruct::m_int_value)
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
