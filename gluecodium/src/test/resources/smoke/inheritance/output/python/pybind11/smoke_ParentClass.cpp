

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentClass = ::gluecodium::smoke::ParentClass;

void register_ParentClass(py::module_& module) {
    py::class_<ParentClass, std::shared_ptr<ParentClass>>(module, "ParentClass")
        .def("root_method", &ParentClass::root_method)
        .def_property("root_property", py::overload_cast<>(&ParentClass::get_root_property, py::const_), py::overload_cast<const ::std::string&>(&ParentClass::set_root_property))
        ;
}

