

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
#include "smoke/DateDefaults.h"
#include "chrono"

using DateDefaults = ::smoke::DateDefaults;



void register_smoke_DateDefaults(py::module_& module) {
auto cls_DateDefaults = py::class_<DateDefaults>(module, "smoke_DateDefaults")
        .def_property("date_time", [](const DateDefaults& self) -> decltype(auto) {
            return
                (self.date_time)
            ;
        }, [](DateDefaults& self, const ::std::chrono::system_clock::time_point& value) {

                self.date_time = value;

        })
        .def_property("date_time_utc", [](const DateDefaults& self) -> decltype(auto) {
            return
                (self.date_time_utc)
            ;
        }, [](DateDefaults& self, const ::std::chrono::system_clock::time_point& value) {

                self.date_time_utc = value;

        })
        .def_property("before_epoch", [](const DateDefaults& self) -> decltype(auto) {
            return
                (self.before_epoch)
            ;
        }, [](DateDefaults& self, const ::std::chrono::system_clock::time_point& value) {

                self.before_epoch = value;

        })
        .def_property("exactly_epoch", [](const DateDefaults& self) -> decltype(auto) {
            return
                (self.exactly_epoch)
            ;
        }, [](DateDefaults& self, const ::std::chrono::system_clock::time_point& value) {

                self.exactly_epoch = value;

        })
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point>(), py::arg("date_time"), py::arg("date_time_utc"), py::arg("before_epoch"), py::arg("exactly_epoch"))
        ;


}
