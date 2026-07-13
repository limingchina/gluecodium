

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Rectangle.h"
#include "cstdint"

void register_Rectangle(py::module_& module) {
    py::class_<Rectangle>(module, "Rectangle")
        .def_readwrite("left", &Rectangle::left)
        .def_readwrite("top", &Rectangle::top)
        .def_readwrite("width", &Rectangle::width)
        .def_readwrite("height", &Rectangle::height)
        ;
}

