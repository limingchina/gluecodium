

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
#include "smoke/MultipleAttributesCpp.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesCpp = ::smoke::MultipleAttributesCpp;


void register_smoke_MultipleAttributesCpp(py::module_& module) {
    py::class_<MultipleAttributesCpp, std::shared_ptr<MultipleAttributesCpp>>(module, "smoke_MultipleAttributesCpp")
        .def("no_lists2", &MultipleAttributesCpp::no_lists2)
        .def("no_lists3", &MultipleAttributesCpp::no_lists3)
        .def("list_first", &MultipleAttributesCpp::list_first)
        .def("list_second", &MultipleAttributesCpp::list_second)
        .def("two_lists", &MultipleAttributesCpp::two_lists)
        ;
}

