

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SpecialNames.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SpecialNames = ::smoke::SpecialNames;

void register_SpecialNames(py::module_& module) {
    py::class_<SpecialNames, std::shared_ptr<SpecialNames>>(module, "SpecialNames")
        .def("create", &SpecialNames::create)
        .def("release", &SpecialNames::release)
        .def("create_proxy", &SpecialNames::create_proxy)
        .def("_uppercase", &SpecialNames::_uppercase)
        .def("make", &SpecialNames::make, py::arg("result"))
        ;
}

