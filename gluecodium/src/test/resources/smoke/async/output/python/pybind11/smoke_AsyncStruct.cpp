

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AsyncStruct.h"
#include "smoke/ThrowMe.h"
#include "cstdint"
#include "string"

void register_AsyncStruct(py::module_& module) {
    py::class_<AsyncStruct>(module, "AsyncStruct")
        .def_readwrite("string_field", &AsyncStruct::string_field)
        .def("async_void", &AsyncStruct::async_void, py::arg("input"))
        .def("async_void_throws", &AsyncStruct::async_void_throws, py::arg("input"))
        .def("async_int", &AsyncStruct::async_int, py::arg("input"))
        .def("async_int_throws", &AsyncStruct::async_int_throws, py::arg("input"))
        .def("async_static", &AsyncStruct::async_static, py::arg("input"))
        ;
}

