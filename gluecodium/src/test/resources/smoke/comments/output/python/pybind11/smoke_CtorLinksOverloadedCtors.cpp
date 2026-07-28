

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
#include "smoke/CtorLinks.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OverloadedCtors = ::smoke::CtorLinks::OverloadedCtors;


void register_smoke_CtorLinksOverloadedCtors(py::module_& module) {
    py::class_<OverloadedCtors, std::shared_ptr<OverloadedCtors>>(module, "smoke_CtorLinksOverloadedCtors")
        .def("__gluecodium_id__", [](const OverloadedCtors& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", py::overload_cast<const ::std::string&>(OverloadedCtors::create), py::arg("input"))
        .def_static("create", py::overload_cast<const ::std::string&, const bool>(OverloadedCtors::create), py::arg("input"), py::arg("flag"))
        ;
}

