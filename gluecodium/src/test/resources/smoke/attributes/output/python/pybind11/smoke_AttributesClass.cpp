

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/AttributesClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AttributesClass = ::smoke::AttributesClass;


void register_smoke_AttributesClass(py::module_& module) {
    py::class_<AttributesClass, std::shared_ptr<AttributesClass>>(module, "AttributesClass")
        .def_property("prop", py::overload_cast<>(&AttributesClass::get_prop, py::const_), py::overload_cast<const ::std::string&>(&AttributesClass::set_prop))
        ;
}

