

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/KotlinInternalClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using KotlinInternalClass = ::gluecodium::smoke::KotlinInternalClass;

void register_KotlinInternalClass(py::module_& module) {
    py::class_<KotlinInternalClass, std::shared_ptr<KotlinInternalClass>>(module, "KotlinInternalClass")
        ;
}

