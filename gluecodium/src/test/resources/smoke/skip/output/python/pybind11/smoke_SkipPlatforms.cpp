

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipPlatforms.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipPlatforms = ::smoke::SkipPlatforms;


void register_smoke_SkipPlatforms(py::module_& module) {
    py::class_<SkipPlatforms, std::shared_ptr<SkipPlatforms>>(module, "SkipPlatforms")
        ;
}

