

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "smoke/PosDefaultsWithDuration.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PosDefaultsWithDuration = ::gluecodium::smoke::PosDefaultsWithDuration;

void register_PosDefaultsWithDuration(py::module_& module) {
    py::class_<PosDefaultsWithDuration>(module, "PosDefaultsWithDuration")
        .def_readwrite("duration_field", &PosDefaultsWithDuration::duration_field)
        .def_readwrite("nanos_field", &PosDefaultsWithDuration::nanos_field)
        ;
}

