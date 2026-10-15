

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
#include "smoke/StructsWithConstants.h"
#include "string"

using StructsWithConstants = ::smoke::StructsWithConstants;
using Route = ::smoke::StructsWithConstants::Route;



void register_smoke_StructsWithConstants(py::module_& module) {
auto cls_StructsWithConstants = py::class_<StructsWithConstants>(module, "smoke_StructsWithConstants")
        .def(py::init<>())
        ;

auto cls_StructsWithConstantsRoute = py::class_<Route>(cls_StructsWithConstants, "Route")
        .def_property("description", [](const Route& self) -> decltype(auto) {
            return
                (self.description)
            ;
        }, [](Route& self, const ::std::string& value) {

                self.description = value;

        })
        .def_property("type", [](const Route& self) -> decltype(auto) {
            return
                (self.type)
            ;
        }, [](Route& self, const ::smoke::RouteUtils::RouteType value) {

                self.type = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string, ::smoke::RouteUtils::RouteType>(), py::arg("description"), py::arg("type"))
        ;


}
