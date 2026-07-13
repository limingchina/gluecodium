

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CppRefReturnType.h"
#include "memory"
#include "optional"
#include "string"

void register_CppRefReturnType(py::module_& module) {
    py::class_<CppRefReturnType>(module, "CppRefReturnType")
        .def("void_ref", &CppRefReturnType::void_ref)
        .def("bool_ref", &CppRefReturnType::bool_ref)
        .def("string_ref", &CppRefReturnType::string_ref)
        .def("struct_ref", &CppRefReturnType::struct_ref)
        .def("class_ref", &CppRefReturnType::class_ref)
        .def("nullable_ref", &CppRefReturnType::nullable_ref)
        .def("throwing_enum_with_void", &CppRefReturnType::throwing_enum_with_void)
        .def("throwing_enum_with_string", &CppRefReturnType::throwing_enum_with_string)
        .def("throwing_struct_with_void", &CppRefReturnType::throwing_struct_with_void)
        .def("throwing_struct_with_string", &CppRefReturnType::throwing_struct_with_string)
        .def_property("string_property", &CppRefReturnType::get_string_property)
        ;
}

