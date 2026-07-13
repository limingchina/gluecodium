

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "smoke/DurationDefaults.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationDefaults = ::smoke::DurationDefaults;

void register_DurationDefaults(py::module_& module) {
    py::class_<DurationDefaults>(module, "DurationDefaults")
        .def_readwrite("dayz", &DurationDefaults::dayz)
        .def_readwrite("hourz", &DurationDefaults::hourz)
        .def_readwrite("minutez", &DurationDefaults::minutez)
        .def_readwrite("secondz", &DurationDefaults::secondz)
        .def_readwrite("milliz", &DurationDefaults::milliz)
        .def_readwrite("microz", &DurationDefaults::microz)
        .def_readwrite("nanoz", &DurationDefaults::nanoz)
        .def(py::init<>())
        ;
}

