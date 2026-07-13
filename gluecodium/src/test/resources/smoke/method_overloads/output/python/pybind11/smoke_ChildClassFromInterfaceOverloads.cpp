

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassFromInterfaceOverloads.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildClassFromInterfaceOverloads = ::smoke::ChildClassFromInterfaceOverloads;

void register_ChildClassFromInterfaceOverloads(py::module_& module) {
    py::class_<ChildClassFromInterfaceOverloads, std::shared_ptr<ChildClassFromInterfaceOverloads>>(module, "ChildClassFromInterfaceOverloads")
        .def("foo", &ChildClassFromInterfaceOverloads::foo, py::arg("input"))
        .def("foo", &ChildClassFromInterfaceOverloads::foo, py::arg("input"))
        .def("bar", &ChildClassFromInterfaceOverloads::bar, py::arg("input"))
        .def("bar", &ChildClassFromInterfaceOverloads::bar, py::arg("input"))
        ;
}

