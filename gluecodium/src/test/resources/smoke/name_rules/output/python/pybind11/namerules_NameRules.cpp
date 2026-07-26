

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
#include "VectorHash.h"
#include "namerules/NameRules.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NameRules = ::namerules::NameRules;


void register_namerules_NameRules(py::module_& module) {
    py::class_<NameRules, std::shared_ptr<NameRules>>(module, "namerules_NameRules")
        .def_static("create", &NameRules::create)
        .def("some_method", &NameRules::someMethod, py::arg("some_argument"))
        .def_property("int_property", py::overload_cast<>(&NameRules::retrieve_int_property, py::const_), py::overload_cast<const uint32_t>(&NameRules::STORE_INT_PROPERTY_NOW))
        .def_property("is_boolean_property", py::overload_cast<>(&NameRules::really_boolean_property, py::const_), py::overload_cast<const bool>(&NameRules::STORE_BOOLEAN_PROPERTY_NOW))
        .def_property("struct_property", py::overload_cast<>(&NameRules::retrieve_struct_property, py::const_), py::overload_cast<const ::namerules::NameRules::ExampleStruct&>(&NameRules::STORE_STRUCT_PROPERTY_NOW))
        ;
}

