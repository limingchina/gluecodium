

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/NullableOverloads.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableOverloads = ::smoke::NullableOverloads;


void register_NullableOverloads(py::module_& module) {
    py::class_<NullableOverloads, std::shared_ptr<NullableOverloads>>(module, "NullableOverloads")
        .def("foo", py::overload_cast<const ::std::string&>(&NullableOverloads::foo), py::arg("input"))

        .def("foo", py::overload_cast<const std::optional< ::std::string >&>(&NullableOverloads::foo), py::arg("input"))

        ;
}

