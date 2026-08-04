

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/EquatableStructWithInternalFields.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using EquatableStructWithInternalFields = ::smoke::EquatableStructWithInternalFields;



void register_smoke_EquatableStructWithInternalFields(py::module_& module) {
auto cls_EquatableStructWithInternalFields = py::class_<EquatableStructWithInternalFields>(module, "smoke_EquatableStructWithInternalFields")
        .def_readwrite("public_field", &EquatableStructWithInternalFields::public_field)
        .def_readwrite("_internal_field", &EquatableStructWithInternalFields::internal_field)
        .def_readwrite("_internal_list_field", &EquatableStructWithInternalFields::internal_list_field)
        .def_readwrite("_internal_map_field", &EquatableStructWithInternalFields::internal_map_field)
        .def_readwrite("_internal_set_field", &EquatableStructWithInternalFields::internal_set_field)
        .def(py::init<>())
        .def(py::init([](const ::std::string& public_field) {
            return EquatableStructWithInternalFields(public_field, ::std::string{}, ::std::vector< ::std::string >{}, ::std::unordered_map< ::std::string, ::std::string >{}, ::std::unordered_set< ::std::string >{});
        }), py::arg("public_field"))
        .def("__eq__", [](const EquatableStructWithInternalFields& lhs, const EquatableStructWithInternalFields& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableStructWithInternalFields& self) { return gluecodium::hash<EquatableStructWithInternalFields>{}(self); })
        ;


}
