

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
#include "smoke/EnableIfSkipped.h"

using EnableIfSkipped = ::smoke::EnableIfSkipped;



void register_smoke_EnableIfSkipped(py::module_& module) {
auto cls_EnableIfSkipped = py::class_<EnableIfSkipped, std::shared_ptr<EnableIfSkipped>>(module, "smoke_EnableIfSkipped")
        .def("__gluecodium_id__", [](const EnableIfSkipped& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
