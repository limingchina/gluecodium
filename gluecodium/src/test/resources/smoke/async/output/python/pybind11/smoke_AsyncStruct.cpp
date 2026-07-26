

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/AsyncStruct.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AsyncStruct = ::smoke::AsyncStruct;

void register_smoke_AsyncStruct(py::module_& module) {
    py::class_<AsyncStruct>(module, "smoke_AsyncStruct")
        .def_readwrite("string_field", &AsyncStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def("async_void", &AsyncStruct::async_void, py::arg("input"))
        .def("async_void_throws", &AsyncStruct::async_void_throws, py::arg("input"))
        .def("async_int", &AsyncStruct::async_int, py::arg("input"))
        .def("async_int_throws", &AsyncStruct::async_int_throws, py::arg("input"))
        .def_static("async_static", &AsyncStruct::async_static, py::arg("input"))
        ;
}

