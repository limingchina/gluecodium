

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
#include "smoke/SkipPlatforms.h"
#include "string"

using SkipPlatforms = ::smoke::SkipPlatforms;



void register_smoke_SkipPlatforms(py::module_& module) {
auto cls_SkipPlatforms = py::class_<SkipPlatforms, std::shared_ptr<SkipPlatforms>>(module, "smoke_SkipPlatforms")
        .def("__gluecodium_id__", [](const SkipPlatforms& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("not_in_java", &SkipPlatforms::not_in_java, py::arg("input"))
        .def_static("not_in_swift", &SkipPlatforms::not_in_swift, py::arg("input"))
        .def_static("not_in_dart", &SkipPlatforms::not_in_dart, py::arg("input"))
        .def_static("not_in_kotlin", &SkipPlatforms::not_in_kotlin, py::arg("input"))
        ;


}
