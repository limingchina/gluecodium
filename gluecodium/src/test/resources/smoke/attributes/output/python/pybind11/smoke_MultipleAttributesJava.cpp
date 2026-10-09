

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
#include "smoke/MultipleAttributesJava.h"

using MultipleAttributesJava = ::smoke::MultipleAttributesJava;



void register_smoke_MultipleAttributesJava(py::module_& module) {
auto cls_MultipleAttributesJava = py::class_<MultipleAttributesJava, std::shared_ptr<MultipleAttributesJava>>(module, "smoke_MultipleAttributesJava")
        .def("__gluecodium_id__", [](const MultipleAttributesJava& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("no_lists2", &MultipleAttributesJava::no_lists2, py::call_guard<py::gil_scoped_release>())
        .def("no_lists3", &MultipleAttributesJava::no_lists3, py::call_guard<py::gil_scoped_release>())
        .def("list_first", &MultipleAttributesJava::list_first, py::call_guard<py::gil_scoped_release>())
        .def("list_second", &MultipleAttributesJava::list_second, py::call_guard<py::gil_scoped_release>())
        .def("two_lists", &MultipleAttributesJava::two_lists, py::call_guard<py::gil_scoped_release>())
        ;


}
