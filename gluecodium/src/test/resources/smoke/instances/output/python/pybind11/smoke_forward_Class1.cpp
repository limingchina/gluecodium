

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/forward/Class1.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Class1 = ::gluecodium::smoke::forward::Class1;

void register_Class1(py::module_& module) {
    py::class_<Class1>(module, "Class1")
        ;
}

