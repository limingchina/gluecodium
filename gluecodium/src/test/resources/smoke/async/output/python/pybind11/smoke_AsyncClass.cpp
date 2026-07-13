

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Async.h"
#include "smoke/AsyncClass.h"
#include "smoke/AsyncErrorCode.h"
#include "cstdint"

void register_AsyncClass(py::module_& module) {
    py::class_<AsyncClass>(module, "AsyncClass")
        .def("async_void", &AsyncClass::async_void, py::arg("input"))
        .def("async_void_throws", &AsyncClass::async_void_throws, py::arg("input"))
        .def("async_int", &AsyncClass::async_int, py::arg("input"))
        .def("async_int_throws", &AsyncClass::async_int_throws, py::arg("input"))
        .def("async_static", &AsyncClass::async_static, py::arg("input"))
        ;
}

