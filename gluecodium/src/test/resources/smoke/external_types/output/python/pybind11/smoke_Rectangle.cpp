

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
#include "smoke/Rectangle.h"
#include "cstdint"

using Rectangle = ::smoke::Rectangle;



void register_smoke_Rectangle(py::module_& module) {
auto cls_Rectangle = py::class_<Rectangle>(module, "smoke_Rectangle")
        .def_readwrite("left", &Rectangle::left)
        .def_readwrite("top", &Rectangle::top)
        .def_readwrite("width", &Rectangle::width)
        .def_readwrite("height", &Rectangle::height)
        .def(py::init<>())
        .def(py::init<int32_t, int32_t, int32_t, int32_t>(), py::arg("left"), py::arg("top"), py::arg("width"), py::arg("height"))
        ;


}
