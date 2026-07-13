

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "package/Class.h"
#include "package/Types.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Class = ::gluecodium::package::class;

void register_Class(py::module_& module) {
    py::class_<Class>(module, "Class")
        .def("constructor", &Class::constructor)
        .def("fun", &Class::fun, py::arg("double"))
        .def_property("property", py::overload_cast<>(&Class::get_property, py::const_), py::overload_cast<const ::package::Types::Enum>(&Class::set_property))
        ;
}

