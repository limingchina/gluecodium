

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
#include "gluecodium/Optional.h"
#include "smoke/CppRefReturnType.h"
#include "memory"
#include "string"

using CppRefReturnType = ::smoke::CppRefReturnType;
using SomeStruct = ::smoke::CppRefReturnType::SomeStruct;
using InternalError = ::smoke::CppRefReturnType::InternalError;



void register_smoke_CppRefReturnType(py::module_& module) {
auto cls_CppRefReturnType = py::class_<CppRefReturnType, std::shared_ptr<CppRefReturnType>>(module, "smoke_CppRefReturnType")
        .def("__gluecodium_id__", [](const CppRefReturnType& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("void_ref", &CppRefReturnType::void_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("bool_ref", &CppRefReturnType::bool_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("string_ref", &CppRefReturnType::string_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("struct_ref", &CppRefReturnType::struct_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("class_ref", &CppRefReturnType::class_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("nullable_ref", &CppRefReturnType::nullable_ref, py::call_guard<py::gil_scoped_release>())
        .def_static("throwing_enum_with_void", []() {
                const auto error = gluecodium::python::call_native([&]() -> decltype(auto) { return CppRefReturnType::throwing_enum_with_void(); });
                if (error) {
                    throw error;
                }
        })
        .def_static("throwing_enum_with_string", &CppRefReturnType::throwing_enum_with_string, py::call_guard<py::gil_scoped_release>())
        .def_static("throwing_struct_with_void", &CppRefReturnType::throwing_struct_with_void, py::call_guard<py::gil_scoped_release>())
        .def_static("throwing_struct_with_string", &CppRefReturnType::throwing_struct_with_string, py::call_guard<py::gil_scoped_release>())
        .def_static("string_property", []() -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return CppRefReturnType::get_string_property();
            });
        })
        ;

auto cls_CppRefReturnTypeSomeStruct = py::class_<SomeStruct>(cls_CppRefReturnType, "SomeStruct")
        .def_property("field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.field)
            ;
        }, [](SomeStruct& self, const ::std::string& value) {

                self.field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;

auto cls_CppRefReturnTypeInternalError = py::enum_<InternalError>(cls_CppRefReturnType, "InternalError")
        .value("FOO", InternalError::FOO)
        .value("BAR", InternalError::BAR)
        ;

    static py::exception<::std::error_code> exc_EnumBasedError(cls_CppRefReturnType, "EnumBasedError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_EnumBasedError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_EnumBasedError.ptr());

    static auto get_py_exc_StructBasedError = []() -> PyObject* {
        static py::object exception;
        if (!exception) {
            exception = py::module_::import("smoke.CppRefReturnType").attr("CppRefReturnType").attr("StructBasedError");
        }
        return exception.ptr();
    };
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::smoke::CppRefReturnType::SomeStruct& e) {
            const auto message = pybind11::detail::ReturnErrorToString<::smoke::CppRefReturnType::SomeStruct>::convert(e);
            PyErr_SetString(get_py_exc_StructBasedError(), message.c_str());
        }
    });
    pybind11::detail::registerReturnError<::smoke::CppRefReturnType::SomeStruct>(get_py_exc_StructBasedError);


}
