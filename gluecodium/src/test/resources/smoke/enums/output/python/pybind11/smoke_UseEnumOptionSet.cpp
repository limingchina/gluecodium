

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/EnumOptionSet.h"
#include "smoke/UseEnumOptionSet.h"
#include "unordered_set"

void register_UseEnumOptionSet(py::module_& module) {
    py::class_<UseEnumOptionSet>(module, "UseEnumOptionSet")
        .def_readwrite("set_field", &UseEnumOptionSet::set_field)
        .def_readwrite("set_field_empty", &UseEnumOptionSet::set_field_empty)
        .def_readwrite("set_field_value", &UseEnumOptionSet::set_field_value)
        .def("round_trip", &UseEnumOptionSet::round_trip, py::arg("input"))
        ;
}

