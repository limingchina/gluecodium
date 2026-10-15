

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
#include "gluecodium/TimePointHash.h"
#include "smoke/DateAlias.h"
#include "smoke/DateDefaultsAliased.h"
#include "chrono"

using DateDefaultsAliased = ::smoke::DateDefaultsAliased;



void register_smoke_DateDefaultsAliased(py::module_& module) {
auto cls_DateDefaultsAliased = py::class_<DateDefaultsAliased>(module, "smoke_DateDefaultsAliased")
        .def_property("date_time", [](const DateDefaultsAliased& self) -> decltype(auto) {
            return
                (self.date_time)
            ;
        }, [](DateDefaultsAliased& self, const ::std::chrono::system_clock::time_point& value) {

                self.date_time = value;

        })
        .def_property("date_time_utc", [](const DateDefaultsAliased& self) -> decltype(auto) {
            return
                (self.date_time_utc)
            ;
        }, [](DateDefaultsAliased& self, const ::std::chrono::system_clock::time_point& value) {

                self.date_time_utc = value;

        })
        .def_property("before_epoch", [](const DateDefaultsAliased& self) -> decltype(auto) {
            return
                (self.before_epoch)
            ;
        }, [](DateDefaultsAliased& self, const ::std::chrono::system_clock::time_point& value) {

                self.before_epoch = value;

        })
        .def_property("exactly_epoch", [](const DateDefaultsAliased& self) -> decltype(auto) {
            return
                (self.exactly_epoch)
            ;
        }, [](DateDefaultsAliased& self, const ::std::chrono::system_clock::time_point& value) {

                self.exactly_epoch = value;

        })
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point>(), py::arg("date_time"), py::arg("date_time_utc"), py::arg("before_epoch"), py::arg("exactly_epoch"))
        ;


}
