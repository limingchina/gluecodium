

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using RouteType = ::smoke::RouteUtils::RouteType;

void register_smoke_RouteUtilsRouteType(py::module_& module) {
    py::enum_<RouteType>(module, "RouteUtilsRouteType")
        .value("NONE", RouteType::NONE)
        .value("CAR", RouteType::CAR)
        .value("PEDESTRIAN", RouteType::PEDESTRIAN)
        .value("EQUESTRIAN", RouteType::EQUESTRIAN)
        ;
}

