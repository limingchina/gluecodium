

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
#include "smoke/MultipleAttributesCpp.h"

using MultipleAttributesCpp = ::smoke::MultipleAttributesCpp;



void register_smoke_MultipleAttributesCpp(py::module_& module) {
auto cls_MultipleAttributesCpp = py::class_<MultipleAttributesCpp, std::shared_ptr<MultipleAttributesCpp>>(module, "smoke_MultipleAttributesCpp")
        .def("__gluecodium_id__", [](const MultipleAttributesCpp& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("no_lists2", &MultipleAttributesCpp::no_lists2, py::call_guard<py::gil_scoped_release>())
        .def("no_lists3", &MultipleAttributesCpp::no_lists3, py::call_guard<py::gil_scoped_release>())
        .def("list_first", &MultipleAttributesCpp::list_first, py::call_guard<py::gil_scoped_release>())
        .def("list_second", &MultipleAttributesCpp::list_second, py::call_guard<py::gil_scoped_release>())
        .def("two_lists", &MultipleAttributesCpp::two_lists, py::call_guard<py::gil_scoped_release>())
        ;


}
