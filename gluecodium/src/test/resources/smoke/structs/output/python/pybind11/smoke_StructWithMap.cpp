

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/StructWithMap.h"
#include "string"
#include "unordered_map"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithMap = ::smoke::StructWithMap;

void register_StructWithMap(py::module_& module) {
    py::class_<StructWithMap>(module, "StructWithMap")
        .def_readwrite("field", &StructWithMap::field)
        .def(py::init<>())
        .def(py::init<::std::unordered_map< ::std::string, ::smoke::StructWithMap >>(), py::arg("field"))
        ;
}

