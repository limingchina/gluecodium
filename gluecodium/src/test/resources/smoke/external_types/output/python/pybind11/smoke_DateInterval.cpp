

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "smoke/DateInterval.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DateInterval = ::gluecodium::smoke::DateInterval;

void register_DateInterval(py::module_& module) {
    py::class_<DateInterval>(module, "DateInterval")
        .def_readwrite("start", &DateInterval::start)
        .def_readwrite("end", &DateInterval::end)
        ;
}

