

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "VectorHash.h"
#include "namerules/NameRules.h"
#include "cstdint"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExampleStruct = ::namerules::NameRules::ExampleStruct;

void register_NameRulesExampleStruct(py::module_& module) {
    py::class_<ExampleStruct>(module, "NameRulesExampleStruct")
        .def_readwrite("value", &ExampleStruct::m_value)
        .def_readwrite("int_value", &ExampleStruct::m_int_value)
        .def(py::init<>())
        .def(py::init<double, ::std::vector< int64_t >>(), py::arg("value"), py::arg("int_value"))
        ;
}

