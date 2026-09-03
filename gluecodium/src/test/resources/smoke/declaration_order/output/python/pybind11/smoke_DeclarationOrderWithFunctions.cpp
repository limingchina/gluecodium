

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
#include "smoke/DeclarationOrderWithFunctions.h"
#include "string"

using DeclarationOrderWithFunctions = ::smoke::DeclarationOrderWithFunctions;
using MainStructWithFunctions = ::smoke::DeclarationOrderWithFunctions::MainStructWithFunctions;
using FieldStruct = ::smoke::DeclarationOrderWithFunctions::FieldStruct;
using ParameterStruct = ::smoke::DeclarationOrderWithFunctions::ParameterStruct;
using ReturnStruct = ::smoke::DeclarationOrderWithFunctions::ReturnStruct;
using ThrownStruct = ::smoke::DeclarationOrderWithFunctions::ThrownStruct;



void register_smoke_DeclarationOrderWithFunctions(py::module_& module) {
auto cls_DeclarationOrderWithFunctions = py::class_<DeclarationOrderWithFunctions>(module, "smoke_DeclarationOrderWithFunctions")
        .def(py::init<>())
        ;

auto cls_DeclarationOrderWithFunctionsMainStructWithFunctions = py::class_<MainStructWithFunctions>(cls_DeclarationOrderWithFunctions, "MainStructWithFunctions")
        .def_readwrite("struct_field", &MainStructWithFunctions::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::DeclarationOrderWithFunctions::FieldStruct>(), py::arg("struct_field"))
        .def("with_parameter", &MainStructWithFunctions::with_parameter, py::arg("input"))
        .def("with_return", &MainStructWithFunctions::with_return)
        .def("with_thrown", &MainStructWithFunctions::with_thrown)
        ;

auto cls_DeclarationOrderWithFunctionsFieldStruct = py::class_<FieldStruct>(cls_DeclarationOrderWithFunctions, "FieldStruct")
        .def_readwrite("some_field", &FieldStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_DeclarationOrderWithFunctionsParameterStruct = py::class_<ParameterStruct>(cls_DeclarationOrderWithFunctions, "ParameterStruct")
        .def_readwrite("some_field", &ParameterStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_DeclarationOrderWithFunctionsReturnStruct = py::class_<ReturnStruct>(cls_DeclarationOrderWithFunctions, "ReturnStruct")
        .def_readwrite("some_field", &ReturnStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_DeclarationOrderWithFunctionsThrownStruct = py::class_<ThrownStruct>(cls_DeclarationOrderWithFunctions, "ThrownStruct")
        .def_readwrite("some_field", &ThrownStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

    static auto get_py_exc_FooBarError = []() -> PyObject* {
        static py::object exception;
        if (!exception) {
            exception = py::module_::import("smoke.DeclarationOrderWithFunctions").attr("DeclarationOrderWithFunctions").attr("FooBarError");
        }
        return exception.ptr();
    };
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::smoke::DeclarationOrderWithFunctions::ThrownStruct& e) {
            const auto message = pybind11::detail::ReturnErrorToString<::smoke::DeclarationOrderWithFunctions::ThrownStruct>::convert(e);
            PyErr_SetString(get_py_exc_FooBarError(), message.c_str());
        }
    });
    pybind11::detail::registerReturnError<::smoke::DeclarationOrderWithFunctions::ThrownStruct>(get_py_exc_FooBarError);


}
