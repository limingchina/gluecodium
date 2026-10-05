

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
#include "gluecodium/DurationHash.h"
#include "smoke/PosDefaultsWithDuration.h"
#include "chrono"

using PosDefaultsWithDuration = ::smoke::PosDefaultsWithDuration;



void register_smoke_PosDefaultsWithDuration(py::module_& module) {
auto cls_PosDefaultsWithDuration = py::class_<PosDefaultsWithDuration>(module, "smoke_PosDefaultsWithDuration")
        .def_property("duration_field", [](const PosDefaultsWithDuration& self) -> decltype(auto) {
            return
                (self.duration_field)
            ;
        }, [](PosDefaultsWithDuration& self, const ::std::chrono::seconds value) {

                self.duration_field = value;

        })
        .def_property("nanos_field", [](const PosDefaultsWithDuration& self) -> decltype(auto) {
            return
                (self.nanos_field)
            ;
        }, [](PosDefaultsWithDuration& self, const ::std::chrono::seconds value) {

                self.nanos_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::chrono::seconds, ::std::chrono::seconds>(), py::arg("duration_field"), py::arg("nanos_field"))
        ;


}
