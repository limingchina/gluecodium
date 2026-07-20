

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MultipleAttributesKotlin.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesKotlin = ::smoke::MultipleAttributesKotlin;


void register_MultipleAttributesKotlin(py::module_& module) {
    py::class_<MultipleAttributesKotlin, std::shared_ptr<MultipleAttributesKotlin>>(module, "MultipleAttributesKotlin")
        .def("no_lists2", &MultipleAttributesKotlin::no_lists2)

        .def("no_lists3", &MultipleAttributesKotlin::no_lists3)

        .def("list_first", &MultipleAttributesKotlin::list_first)

        .def("list_second", &MultipleAttributesKotlin::list_second)

        .def("two_lists", &MultipleAttributesKotlin::two_lists)

        ;
}

