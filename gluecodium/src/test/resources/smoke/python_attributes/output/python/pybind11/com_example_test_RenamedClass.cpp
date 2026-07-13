

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "com/example/test/MyClass.h"
#include "cstdint"
#include "string"

void register_RenamedClass(py::module_& module) {
    py::class_<MyClass>(module, "RenamedClass")
        .def("hidden_method", &MyClass::hidden_method)
        .def("internal_method", &MyClass::internal_method)
        .def("visible_method", &MyClass::visible_method, py::arg("param"))
        ;
}

