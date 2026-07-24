

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/TypeCollection.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Line = ::smoke::TypeCollection::Line;

void register_smoke_TypeCollectionLine(py::module_& module) {
    py::class_<Line>(module, "TypeCollectionLine")
        .def_readwrite("a", &Line::a)
        .def_readwrite("b", &Line::b)
        .def(py::init<>())
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::TypeCollection::Point(), py::arg("a"), py::arg("b"))
        ;
}

