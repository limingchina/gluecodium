

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
#include "smoke/MultipleAttributesDart.h"

using MultipleAttributesDart = ::smoke::MultipleAttributesDart;



void register_smoke_MultipleAttributesDart(py::module_& module) {
auto cls_MultipleAttributesDart = py::class_<MultipleAttributesDart, std::shared_ptr<MultipleAttributesDart>>(module, "smoke_MultipleAttributesDart")
        .def("__gluecodium_id__", [](const MultipleAttributesDart& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("no_lists2", &MultipleAttributesDart::no_lists2, py::call_guard<py::gil_scoped_release>())
        .def("no_lists3", &MultipleAttributesDart::no_lists3, py::call_guard<py::gil_scoped_release>())
        .def("list_first", &MultipleAttributesDart::list_first, py::call_guard<py::gil_scoped_release>())
        .def("list_second", &MultipleAttributesDart::list_second, py::call_guard<py::gil_scoped_release>())
        .def("two_lists", &MultipleAttributesDart::two_lists, py::call_guard<py::gil_scoped_release>())
        ;


}
