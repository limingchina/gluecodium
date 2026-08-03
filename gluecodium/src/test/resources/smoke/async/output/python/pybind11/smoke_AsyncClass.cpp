

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
#include "smoke/AsyncClass.h"
#include "smoke/AsyncErrorCode.h"
#include "cstdint"

using AsyncClass = ::smoke::AsyncClass;



void register_smoke_AsyncClass(py::module_& module) {
auto cls_AsyncClass = py::class_<AsyncClass, std::shared_ptr<AsyncClass>>(module, "smoke_AsyncClass")
        .def("__gluecodium_id__", [](const AsyncClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("async_void", &AsyncClass::async_void, py::arg("input"))
        .def("async_void_throws", &AsyncClass::async_void_throws, py::arg("input"))
        .def("async_int", &AsyncClass::async_int, py::arg("input"))
        .def("async_int_throws", &AsyncClass::async_int_throws, py::arg("input"))
        .def_static("async_static", &AsyncClass::async_static, py::arg("input"))
        ;


}
