

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalClassWithStaticProperty.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalClassWithStaticProperty = ::gluecodium::smoke::InternalClassWithStaticProperty;

void register_InternalClassWithStaticProperty(py::module_& module) {
    py::class_<InternalClassWithStaticProperty>(module, "InternalClassWithStaticProperty")
        .def_property("foo_bar", py::overload_cast<>(&InternalClassWithStaticProperty::get_foo_bar, py::const_), py::overload_cast<const ::std::string&>(&InternalClassWithStaticProperty::set_foo_bar))
        ;
}

