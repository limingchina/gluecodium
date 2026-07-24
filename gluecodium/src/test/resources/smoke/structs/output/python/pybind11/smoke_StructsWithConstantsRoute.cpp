

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/RouteUtils.h"
#include "smoke/StructsWithConstants.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Route = ::smoke::StructsWithConstants::Route;

void register_smoke_StructsWithConstantsRoute(py::module_& module) {
    py::class_<Route>(module, "StructsWithConstantsRoute")
        .def_readwrite("description", &Route::description)
        .def_readwrite("type", &Route::type)
        .def(py::init<>())
        .def(py::init<::std::string, ::smoke::RouteUtils::RouteType(), py::arg("description"), py::arg("type"))
        ;
}

