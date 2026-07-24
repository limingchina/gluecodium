

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalPropertyOnly.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalPropertyOnly = ::smoke::InternalPropertyOnly;


void register_smoke_InternalPropertyOnly(py::module_& module) {
    py::class_<InternalPropertyOnly, std::shared_ptr<InternalPropertyOnly>>(module, "InternalPropertyOnly")
        .def_property("foo", py::overload_cast<>(&InternalPropertyOnly::get_foo, py::const_), py::overload_cast<const ::std::string&>(&InternalPropertyOnly::set_foo))
        ;
}

