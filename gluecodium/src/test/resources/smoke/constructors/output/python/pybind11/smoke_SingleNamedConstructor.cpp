

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
#include "smoke/SingleNamedConstructor.h"
#include "memory"

using SingleNamedConstructor = ::smoke::SingleNamedConstructor;



void register_smoke_SingleNamedConstructor(py::module_& module) {
auto cls_SingleNamedConstructor = py::class_<SingleNamedConstructor, std::shared_ptr<SingleNamedConstructor>>(module, "smoke_SingleNamedConstructor")
        .def("__gluecodium_id__", [](const SingleNamedConstructor& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &SingleNamedConstructor::create)
        ;


}
