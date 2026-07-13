

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ListenerWithNullable.h"
#include "cstdint"
#include "optional"

void register_ListenerWithNullable(py::module_& module) {
    py::class_<ListenerWithNullable, std::shared_ptr<ListenerWithNullable>>(module, "ListenerWithNullable")
        .def("method_with_byte", &ListenerWithNullable::method_with_byte, py::arg("input"))
        .def("method_with_u_byte", &ListenerWithNullable::method_with_u_byte, py::arg("input"))
        .def("method_with_short", &ListenerWithNullable::method_with_short, py::arg("input"))
        .def("method_with_u_short", &ListenerWithNullable::method_with_u_short, py::arg("input"))
        .def("method_with_int", &ListenerWithNullable::method_with_int, py::arg("input"))
        .def("method_with_u_int", &ListenerWithNullable::method_with_u_int, py::arg("input"))
        .def("method_with_long", &ListenerWithNullable::method_with_long, py::arg("input"))
        .def("method_with_u_long", &ListenerWithNullable::method_with_u_long, py::arg("input"))
        .def("method_with_double", &ListenerWithNullable::method_with_double, py::arg("input"))
        .def("method_with_float", &ListenerWithNullable::method_with_float, py::arg("input"))
        .def("method_with_double", &ListenerWithNullable::method_with_double, py::arg("input"))
        ;
}

