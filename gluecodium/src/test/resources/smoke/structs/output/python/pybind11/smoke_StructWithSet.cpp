

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
#include "smoke/StructWithSet.h"
#include "unordered_set"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithSet = ::gluecodium::smoke::StructWithSet;

void register_StructWithSet(py::module_& module) {
    py::class_<StructWithSet>(module, "StructWithSet")
        .def_readwrite("field", &StructWithSet::field)
        .def(py::init<::std::unordered_set< ::smoke::StructWithSet, ::gluecodium::hash< ::smoke::StructWithSet > >>(), py::arg("field"))
        ;
}

