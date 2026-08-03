

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
#include "smoke/SkipFunctions.h"
#include "string"

using SkipFunctions = ::smoke::SkipFunctions;



void register_smoke_SkipFunctions(py::module_& module) {
auto cls_SkipFunctions = py::class_<SkipFunctions, std::shared_ptr<SkipFunctions>>(module, "smoke_SkipFunctions")
        .def("__gluecodium_id__", [](const SkipFunctions& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("not_in_java", &SkipFunctions::not_in_java, py::arg("input"))
        .def_static("not_in_swift", &SkipFunctions::not_in_swift, py::arg("input"))
        .def_static("not_in_dart", &SkipFunctions::not_in_dart, py::arg("input"))
        .def_static("not_in_kotlin", &SkipFunctions::not_in_kotlin, py::arg("input"))
        ;


}
