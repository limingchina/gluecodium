

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
#include "smoke/DartPublicElementsSkipped.h"
#include "string"

using DartPublicElementsSkipped = ::smoke::DartPublicElementsSkipped;



void register_smoke_DartPublicElementsSkipped(py::module_& module) {
auto cls_DartPublicElementsSkipped = py::class_<DartPublicElementsSkipped>(module, "smoke_DartPublicElementsSkipped")
        .def_property("bool_field", [](const DartPublicElementsSkipped& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](DartPublicElementsSkipped& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("_string_field", [](const DartPublicElementsSkipped& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](DartPublicElementsSkipped& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init([](const bool& bool_field) {
            return DartPublicElementsSkipped(bool_field, ::std::string{});
        }), py::arg("bool_field"))
        .def("_foo", &DartPublicElementsSkipped::foo, py::call_guard<py::gil_scoped_release>())
        ;


}
