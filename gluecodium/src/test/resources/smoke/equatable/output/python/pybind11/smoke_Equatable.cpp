

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Equatable.h"
#include "cstdint"
#include "optional"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Equatable = ::gluecodium::smoke::Equatable;

void register_Equatable(py::module_& module) {
    py::class_<Equatable>(module, "Equatable")
        ;
}

