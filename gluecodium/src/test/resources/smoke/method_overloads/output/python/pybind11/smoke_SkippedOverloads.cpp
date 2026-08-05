

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
#include "smoke/SkippedOverloads.h"
#include "memory"
#include "string"

using SkippedOverloads = ::smoke::SkippedOverloads;



void register_smoke_SkippedOverloads(py::module_& module) {
auto cls_SkippedOverloads = py::class_<SkippedOverloads, std::shared_ptr<SkippedOverloads>>(module, "smoke_SkippedOverloads")
        .def("__gluecodium_id__", [](const SkippedOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("make", &SkippedOverloads::make)
        .def_static("make_for_dart", &SkippedOverloads::make_for_dart, py::arg("input"))
        ;


}
