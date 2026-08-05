

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/RouteUtils.h"

using RouteUtils = ::smoke::RouteUtils;
using RouteType = ::smoke::RouteUtils::RouteType;



void register_smoke_RouteUtils(py::module_& module) {
auto cls_RouteUtils = py::class_<RouteUtils>(module, "smoke_RouteUtils")
        .def(py::init<>())
        ;

auto cls_RouteUtilsRouteType = py::enum_<RouteType>(cls_RouteUtils, "RouteType")
        .value("NONE", RouteType::NONE)
        .value("CAR", RouteType::CAR)
        .value("PEDESTRIAN", RouteType::PEDESTRIAN)
        .value("EQUESTRIAN", RouteType::EQUESTRIAN)
        ;


}
