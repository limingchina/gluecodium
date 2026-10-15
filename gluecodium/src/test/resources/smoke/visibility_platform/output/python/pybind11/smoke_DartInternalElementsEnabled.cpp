

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
#include "smoke/DartInternalElementsEnabled.h"
#include "string"

using DartInternalElementsEnabled = ::smoke::DartInternalElementsEnabled;



void register_smoke_DartInternalElementsEnabled(py::module_& module) {
auto cls_DartInternalElementsEnabled = py::class_<DartInternalElementsEnabled>(module, "smoke_DartInternalElementsEnabled")
        .def_property("bool_field", [](const DartInternalElementsEnabled& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](DartInternalElementsEnabled& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("string_field", [](const DartInternalElementsEnabled& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](DartInternalElementsEnabled& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<bool, ::std::string>(), py::arg("bool_field"), py::arg("string_field"))
        .def("foo", &DartInternalElementsEnabled::foo, py::call_guard<py::gil_scoped_release>())
        ;


}
