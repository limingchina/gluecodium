

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
#include "smoke/AttributesWithDeprecated.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AttributesWithDeprecated = ::smoke::AttributesWithDeprecated;


void register_smoke_AttributesWithDeprecated(py::module_& module) {
    py::class_<AttributesWithDeprecated, std::shared_ptr<AttributesWithDeprecated>>(module, "smoke_AttributesWithDeprecated")
        .def("very_fun", &AttributesWithDeprecated::very_fun)
        .def_property("prop", py::overload_cast<>(&AttributesWithDeprecated::get_prop, py::const_), py::overload_cast<const ::std::string&>(&AttributesWithDeprecated::set_prop))
        ;
}

