

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "smoke/DurationMilliseconds.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationStruct = ::smoke::DurationMilliseconds::DurationStruct;

void register_DurationMillisecondsDurationStruct(py::module_& module) {
    py::class_<DurationStruct>(module, "DurationMillisecondsDurationStruct")
        .def_readwrite("duration_field", &DurationStruct::duration_field)
        .def(py::init<>())
        .def(py::init<std::chrono::milliseconds>(), py::arg("duration_field"))
        ;
}

