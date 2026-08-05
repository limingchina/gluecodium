

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
#include "smoke/AsyncRenamed.h"

using AsyncRenamed = ::smoke::AsyncRenamed;



void register_smoke_AsyncRenamed(py::module_& module) {
auto cls_AsyncRenamed = py::class_<AsyncRenamed, std::shared_ptr<AsyncRenamed>>(module, "smoke_AsyncRenamed")
        .def("__gluecodium_id__", [](const AsyncRenamed& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("dispose", &AsyncRenamed::callDispose)
        ;


}
