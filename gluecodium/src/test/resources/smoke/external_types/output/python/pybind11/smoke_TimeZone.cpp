

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/TimeZone.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using TimeZone = ::gluecodium::smoke::TimeZone;

void register_TimeZone(py::module_& module) {
    py::class_<TimeZone>(module, "TimeZone")
        .def_readwrite("raw_offset", &TimeZone::raw_offset)
        ;
}

