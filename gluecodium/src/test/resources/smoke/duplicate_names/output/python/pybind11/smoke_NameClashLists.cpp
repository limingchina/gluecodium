

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Alphabet.h"
#include "smoke/NameClashLists.h"
#include "smoke/foo/Alphabet.h"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NameClashLists = ::gluecodium::smoke::NameClashLists;

void register_NameClashLists(py::module_& module) {
    py::class_<NameClashLists>(module, "NameClashLists")
        .def_readwrite("field_a", &NameClashLists::field_a)
        .def_readwrite("field_b", &NameClashLists::field_b)
        ;
}

