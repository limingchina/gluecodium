

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
#include "smoke/DurationDefaults.h"
#include "chrono"

using DurationDefaults = ::smoke::DurationDefaults;



void register_smoke_DurationDefaults(py::module_& module) {
auto cls_DurationDefaults = py::class_<DurationDefaults>(module, "smoke_DurationDefaults")
        .def_property("dayz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.dayz)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::seconds value) {

                self.dayz = value;

        })
        .def_property("hourz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.hourz)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::seconds value) {

                self.hourz = value;

        })
        .def_property("minutez", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.minutez)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::seconds value) {

                self.minutez = value;

        })
        .def_property("secondz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.secondz)
            ;
        }, [](DurationDefaults& self, const std::chrono::seconds value) {

                self.secondz = value;

        })
        .def_property("milliz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.milliz)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::milliseconds value) {

                self.milliz = value;

        })
        .def_property("microz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.microz)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::seconds value) {

                self.microz = value;

        })
        .def_property("nanoz", [](const DurationDefaults& self) -> decltype(auto) {
            return
                (self.nanoz)
            ;
        }, [](DurationDefaults& self, const ::std::chrono::seconds value) {

                self.nanoz = value;

        })
        .def(py::init<>())
        .def(py::init<::std::chrono::seconds, ::std::chrono::seconds, ::std::chrono::seconds, std::chrono::seconds, ::std::chrono::milliseconds, ::std::chrono::seconds, ::std::chrono::seconds>(), py::arg("dayz"), py::arg("hourz"), py::arg("minutez"), py::arg("secondz"), py::arg("milliz"), py::arg("microz"), py::arg("nanoz"))
        ;


}
