

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MultipleAttributesDart.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesDart = ::smoke::MultipleAttributesDart;


void register_smoke_MultipleAttributesDart(py::module_& module) {
    py::class_<MultipleAttributesDart, std::shared_ptr<MultipleAttributesDart>>(module, "smoke_MultipleAttributesDart")
        .def("no_lists2", &MultipleAttributesDart::no_lists2)
        .def("no_lists3", &MultipleAttributesDart::no_lists3)
        .def("list_first", &MultipleAttributesDart::list_first)
        .def("list_second", &MultipleAttributesDart::list_second)
        .def("two_lists", &MultipleAttributesDart::two_lists)
        ;
}

