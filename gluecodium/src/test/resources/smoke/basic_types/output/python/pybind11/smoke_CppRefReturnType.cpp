

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CppRefReturnType.h"
#include "memory"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CppRefReturnType = ::smoke::CppRefReturnType;

void register_CppRefReturnType(py::module_& module) {
    py::class_<CppRefReturnType, std::shared_ptr<CppRefReturnType>>(module, "CppRefReturnType")
        .def_static("void_ref", &CppRefReturnType::void_ref)
        .def_static("bool_ref", &CppRefReturnType::bool_ref)
        .def_static("string_ref", &CppRefReturnType::string_ref)
        .def_static("struct_ref", &CppRefReturnType::struct_ref)
        .def_static("class_ref", &CppRefReturnType::class_ref)
        .def_static("nullable_ref", &CppRefReturnType::nullable_ref)
        .def_static("throwing_enum_with_void", &CppRefReturnType::throwing_enum_with_void)
        .def_static("throwing_enum_with_string", &CppRefReturnType::throwing_enum_with_string)
        .def_static("throwing_struct_with_void", &CppRefReturnType::throwing_struct_with_void)
        .def_static("throwing_struct_with_string", &CppRefReturnType::throwing_struct_with_string)
        .def_static("string_property", &CppRefReturnType::get_string_property)
        ;
}

