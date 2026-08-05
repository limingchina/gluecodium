

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
#include "smoke/Comments.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"

using Comments = ::smoke::Comments;
using SomeStruct = ::smoke::Comments::SomeStruct;
using SomeEnum = ::smoke::Comments::SomeEnum;



void register_smoke_Comments(py::module_& module) {
auto cls_Comments = py::class_<Comments, std::shared_ptr<Comments>>(module, "smoke_Comments")
        .def("__gluecodium_id__", [](const Comments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_all_comments", &Comments::some_method_with_all_comments, py::arg("input_parameter"))
        .def("some_method_with_input_comments", &Comments::some_method_with_input_comments, py::arg("input"))
        .def("some_method_with_output_comments", &Comments::some_method_with_output_comments, py::arg("input"))
        .def("some_method_with_no_comments", &Comments::some_method_with_no_comments, py::arg("input"))
        .def("some_method_without_return_type_with_all_comments", &Comments::some_method_without_return_type_with_all_comments, py::arg("input"))
        .def("some_method_without_return_type_with_no_comments", &Comments::some_method_without_return_type_with_no_comments, py::arg("input"))
        .def("some_method_without_input_parameters_with_all_comments", &Comments::some_method_without_input_parameters_with_all_comments)
        .def("some_method_without_input_parameters_with_no_comments", &Comments::some_method_without_input_parameters_with_no_comments)
        .def("some_method_with_nothing", &Comments::some_method_with_nothing)
        .def("some_method_without_return_type_or_input_parameters", &Comments::some_method_without_return_type_or_input_parameters)
        .def("one_parameter_comment_only", &Comments::one_parameter_comment_only, py::arg("undocumented"), py::arg("documented"))
        .def("return_comment_only", &Comments::return_comment_only, py::arg("undocumented"))
        .def_property("is_some_property", py::overload_cast<>(&Comments::is_some_property, py::const_), py::overload_cast<const bool>(&Comments::set_some_property))
        .def_property_readonly("only_getter_property", py::overload_cast<>(&Comments::get_only_getter_property, py::const_))
        .def_property("is_is_visible", py::overload_cast<>(&Comments::is_is_visible, py::const_), py::overload_cast<const bool>(&Comments::set_is_visible))
        ;

auto cls_commentsSomeStruct = py::class_<SomeStruct>(cls_Comments, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def_readwrite("nullable_field", &SomeStruct::nullable_field)
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        .def(py::init<bool, std::optional< ::std::string >>(), py::arg("some_field"), py::arg("nullable_field"))
        .def("some_struct_method", &SomeStruct::some_struct_method)
        .def_static("some_static_struct_method", &SomeStruct::some_static_struct_method)
        ;

auto cls_commentsSomeEnum = py::enum_<SomeEnum>(cls_Comments, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        .value("USEFUL", SomeEnum::USEFUL)
        ;

    static py::exception<::std::error_code> exc_SomethingWrongError(cls_Comments, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_SomethingWrongError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_SomethingWrongError.ptr());


}
