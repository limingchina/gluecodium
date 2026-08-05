

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
#include "smoke/AsyncWithSkips.h"
#include "string"

using AsyncWithSkips = ::smoke::AsyncWithSkips;



void register_smoke_AsyncWithSkips(py::module_& module) {
auto cls_AsyncWithSkips = py::class_<AsyncWithSkips, std::shared_ptr<AsyncWithSkips>>(module, "smoke_AsyncWithSkips")
        .def("__gluecodium_id__", [](const AsyncWithSkips& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("make_shared_instance", py::overload_cast<const ::std::string&>(&AsyncWithSkips::make_shared_instance), py::arg("android_context"))
        .def_static("make_shared_instance", py::overload_cast<>(&AsyncWithSkips::make_shared_instance))
        ;


}
