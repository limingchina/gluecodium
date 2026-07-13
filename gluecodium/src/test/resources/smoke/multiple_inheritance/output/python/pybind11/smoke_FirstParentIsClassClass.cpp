

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsClassClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsClassClass = ::gluecodium::smoke::FirstParentIsClassClass;

void register_FirstParentIsClassClass(py::module_& module) {
    py::class_<FirstParentIsClassClass>(module, "FirstParentIsClassClass")
        .def("child_function", &FirstParentIsClassClass::child_function)
        .def_property("child_property", py::overload_cast<>(&FirstParentIsClassClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsClassClass::set_child_property))
        ;
}

