

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
#include "smoke/SwiftConstructorOverloads.h"
#include "memory"
#include "string"

using SwiftConstructorOverloads = ::smoke::SwiftConstructorOverloads;



void register_smoke_SwiftConstructorOverloads(py::module_& module) {
auto cls_SwiftConstructorOverloads = py::class_<SwiftConstructorOverloads, std::shared_ptr<SwiftConstructorOverloads>>(module, "smoke_SwiftConstructorOverloads")
        .def("__gluecodium_id__", [](const SwiftConstructorOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("make", &SwiftConstructorOverloads::make, py::arg("input"))
        .def_static("make_do", &SwiftConstructorOverloads::make_do, py::arg("throughput"))
        ;


}
