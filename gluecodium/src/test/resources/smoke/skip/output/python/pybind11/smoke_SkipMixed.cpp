

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
#include "smoke/SkipMixed.h"

using SkipMixed = ::smoke::SkipMixed;



void register_smoke_SkipMixed(py::module_& module) {
auto cls_SkipMixed = py::class_<SkipMixed, std::shared_ptr<SkipMixed>>(module, "smoke_SkipMixed")
        .def("__gluecodium_id__", [](const SkipMixed& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
