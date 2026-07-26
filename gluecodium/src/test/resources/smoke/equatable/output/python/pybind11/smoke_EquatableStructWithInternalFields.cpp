

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EquatableStructWithInternalFields.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EquatableStructWithInternalFields = ::smoke::EquatableStructWithInternalFields;

void register_smoke_EquatableStructWithInternalFields(py::module_& module) {
    py::class_<EquatableStructWithInternalFields>(module, "smoke_EquatableStructWithInternalFields")
        .def_readwrite("public_field", &EquatableStructWithInternalFields::public_field)
        .def_readwrite("internal_field", &EquatableStructWithInternalFields::internal_field)
        .def_readwrite("internal_list_field", &EquatableStructWithInternalFields::internal_list_field)
        .def_readwrite("internal_map_field", &EquatableStructWithInternalFields::internal_map_field)
        .def_readwrite("internal_set_field", &EquatableStructWithInternalFields::internal_set_field)
        .def(py::init<>())
        .def(py::init<::std::string, ::std::string, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("public_field"), py::arg("internal_field"), py::arg("internal_list_field"), py::arg("internal_map_field"), py::arg("internal_set_field"))
        .def(py::init<::std::string, ::std::string, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("public_field"), py::arg("internal_field"), py::arg("internal_list_field"), py::arg("internal_map_field"), py::arg("internal_set_field"))
        .def(py::init<::std::string, ::std::string, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("public_field"), py::arg("internal_field"), py::arg("internal_list_field"), py::arg("internal_map_field"), py::arg("internal_set_field"))
        .def(py::init<::std::string, ::std::string, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("public_field"), py::arg("internal_field"), py::arg("internal_list_field"), py::arg("internal_map_field"), py::arg("internal_set_field"))
        .def(py::init<::std::string, ::std::string, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("public_field"), py::arg("internal_field"), py::arg("internal_list_field"), py::arg("internal_map_field"), py::arg("internal_set_field"))
        ;
}

