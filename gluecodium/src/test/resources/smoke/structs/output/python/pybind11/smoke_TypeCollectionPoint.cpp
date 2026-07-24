

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
using Point = ::smoke::TypeCollection::Point;

void register_smoke_TypeCollectionPoint(py::module_& module) {
    py::class_<Point>(module, "TypeCollectionPoint")
        .def_readwrite("x", &Point::x)
        .def_readwrite("y", &Point::y)
        .def(py::init<>())
        .def(py::init<double, double(), py::arg("x"), py::arg("y"))
        ;
}

