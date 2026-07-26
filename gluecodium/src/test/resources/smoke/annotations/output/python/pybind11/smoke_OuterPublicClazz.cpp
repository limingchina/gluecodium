

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
#include "smoke/OuterPublicClazz.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterPublicClazz = ::smoke::OuterPublicClazz;


void register_smoke_OuterPublicClazz(py::module_& module) {
    py::class_<OuterPublicClazz, std::shared_ptr<OuterPublicClazz>>(module, "smoke_OuterPublicClazz")
        ;
}

