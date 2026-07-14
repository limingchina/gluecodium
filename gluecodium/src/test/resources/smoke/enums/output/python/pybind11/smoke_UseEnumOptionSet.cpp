

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/EnumOptionSet.h"
#include "smoke/UseEnumOptionSet.h"
#include "unordered_set"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseEnumOptionSet = ::smoke::UseEnumOptionSet;

void register_UseEnumOptionSet(py::module_& module) {
    py::class_<UseEnumOptionSet>(module, "UseEnumOptionSet")
        .def_readwrite("set_field", &UseEnumOptionSet::set_field)
        .def_readwrite("set_field_empty", &UseEnumOptionSet::set_field_empty)
        .def_readwrite("set_field_value", &UseEnumOptionSet::set_field_value)
        .def(py::init<::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >, ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >, ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >>(), py::arg("set_field"), py::arg("set_field_empty"), py::arg("set_field_value"))
        .def_static("round_trip", &UseEnumOptionSet::round_trip, py::arg("input"))
        ;
}

