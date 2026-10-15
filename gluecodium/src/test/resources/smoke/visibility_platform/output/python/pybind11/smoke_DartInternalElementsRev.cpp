

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
#include "smoke/DartInternalElementsRev.h"
#include "string"

using DartInternalElementsRev = ::smoke::DartInternalElementsRev;



void register_smoke_DartInternalElementsRev(py::module_& module) {
auto cls_DartInternalElementsRev = py::class_<DartInternalElementsRev>(module, "smoke_DartInternalElementsRev")
        .def_property("string_field", [](const DartInternalElementsRev& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](DartInternalElementsRev& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def("foo", &DartInternalElementsRev::foo, py::call_guard<py::gil_scoped_release>())
        ;


}
