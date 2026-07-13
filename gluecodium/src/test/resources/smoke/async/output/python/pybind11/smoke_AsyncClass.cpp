

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/AsyncClass.h"
#include "smoke/AsyncErrorCode.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AsyncClass = ::smoke::AsyncClass;

void register_AsyncClass(py::module_& module) {
    py::class_<AsyncClass, std::shared_ptr<AsyncClass>>(module, "AsyncClass")
        .def("async_void", &AsyncClass::async_void, py::arg("input"))
        .def("async_void_throws", &AsyncClass::async_void_throws, py::arg("input"))
        .def("async_int", &AsyncClass::async_int, py::arg("input"))
        .def("async_int_throws", &AsyncClass::async_int_throws, py::arg("input"))
        .def("async_static", &AsyncClass::async_static, py::arg("input"))
        ;
}

