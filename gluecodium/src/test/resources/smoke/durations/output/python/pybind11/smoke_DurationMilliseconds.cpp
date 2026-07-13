

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
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationMilliseconds = ::smoke::DurationMilliseconds;

void register_DurationMilliseconds(py::module_& module) {
    py::class_<DurationMilliseconds, std::shared_ptr<DurationMilliseconds>>(module, "DurationMilliseconds")
        .def("duration_function", &DurationMilliseconds::duration_function, py::arg("input"))
        .def("nullable_duration_function", &DurationMilliseconds::nullable_duration_function, py::arg("input"))
        .def_property("duration_property", py::overload_cast<>(&DurationMilliseconds::get_duration_property, py::const_), py::overload_cast<const std::chrono::milliseconds>(&DurationMilliseconds::set_duration_property))
        ;
}

