

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
#include "smoke/forward/Class1.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Class1 = ::smoke::forward::Class1;


void register_smoke_forward_Class1(py::module_& module) {
    py::class_<Class1, std::shared_ptr<Class1>>(module, "smoke_forward_Class1")
        ;
}

