

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
#include "foo/Bar.h"
#include "cstdint"
#include "string"



void register_smoke_ExternalClass(py::module_& module) {
    py::class_<::fire::Baz, std::shared_ptr<::fire::Baz>>(module, "smoke_ExternalClass")
        .def("__gluecodium_id__", [](const ::fire::Baz& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

