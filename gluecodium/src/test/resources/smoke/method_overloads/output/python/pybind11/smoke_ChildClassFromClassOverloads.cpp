

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassFromClassOverloads.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildClassFromClassOverloads = ::smoke::ChildClassFromClassOverloads;

void register_ChildClassFromClassOverloads(py::module_& module) {
    py::class_<ChildClassFromClassOverloads, std::shared_ptr<ChildClassFromClassOverloads>>(module, "ChildClassFromClassOverloads")
        .def("foo", py::overload_cast<const ::std::string&>(&ChildClassFromClassOverloads::foo), py::arg("input"))
        .def("foo", py::overload_cast<const double>(&ChildClassFromClassOverloads::foo), py::arg("input"))
        .def("bar", py::overload_cast<const ::std::string&>(&ChildClassFromClassOverloads::bar), py::arg("input"))
        .def("bar", py::overload_cast<const double>(&ChildClassFromClassOverloads::bar), py::arg("input"))
        ;
}

