

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "include/ExternalTypes.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ClassWithOverloads = ::smoke::ClassWithOverloads;


void register_smoke_ClassWithOverloads(py::module_& module) {
    py::class_<ClassWithOverloads, std::shared_ptr<ClassWithOverloads>>(module, "ClassWithOverloads")
        ;
}

