

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/BlobDefaults.h"
#include "cstdint"
#include "memory"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using BlobDefaults = ::gluecodium::smoke::BlobDefaults;

void register_BlobDefaults(py::module_& module) {
    py::class_<BlobDefaults>(module, "BlobDefaults")
        .def_readwrite("empty_list", &BlobDefaults::empty_list)
        .def_readwrite("dead_beef", &BlobDefaults::dead_beef)
        ;
}

