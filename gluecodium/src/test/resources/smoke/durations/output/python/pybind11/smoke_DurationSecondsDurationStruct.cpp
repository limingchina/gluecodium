

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
#include "gluecodium/DurationHash.h"
#include "smoke/DurationSeconds.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationStruct = ::smoke::DurationSeconds::DurationStruct;

void register_smoke_DurationSecondsDurationStruct(py::module_& module) {
    py::class_<DurationStruct>(module, "smoke_DurationSecondsDurationStruct")
        .def_readwrite("duration_field", &DurationStruct::duration_field)
        .def(py::init<>())
        .def(py::init<::std::chrono::seconds>(), py::arg("duration_field"))
        ;
}

