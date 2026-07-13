

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "smoke/DurationSeconds.h"
#include "chrono"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationSeconds = ::smoke::DurationSeconds;

void register_DurationSeconds(py::module_& module) {
    py::class_<DurationSeconds, std::shared_ptr<DurationSeconds>>(module, "DurationSeconds")
        .def("duration_function", &DurationSeconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationSeconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", py::overload_cast<>(&DurationSeconds::get_duration_property, py::const_), py::overload_cast<const ::std::chrono::seconds>(&DurationSeconds::set_duration_property))
        ;
}

