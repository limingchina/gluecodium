

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "core/duration.h"
#include "cstdint"


void register_smoke_DurationExternal(py::module_& module) {
    py::class_<std::chrono::duration<uint64_t, std::ratio<1,1000>>>(module, "DurationExternal")
        ;
}

