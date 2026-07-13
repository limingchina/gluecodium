

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MultipleAttributesJava.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesJava = ::gluecodium::smoke::MultipleAttributesJava;

void register_MultipleAttributesJava(py::module_& module) {
    py::class_<MultipleAttributesJava>(module, "MultipleAttributesJava")
        .def("no_lists2", &MultipleAttributesJava::no_lists2)
        .def("no_lists3", &MultipleAttributesJava::no_lists3)
        .def("list_first", &MultipleAttributesJava::list_first)
        .def("list_second", &MultipleAttributesJava::list_second)
        .def("two_lists", &MultipleAttributesJava::two_lists)
        ;
}

