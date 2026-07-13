

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsNarrowClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsNarrowClass = ::smoke::FirstParentIsNarrowClass;

void register_FirstParentIsNarrowClass(py::module_& module) {
    py::class_<FirstParentIsNarrowClass, std::shared_ptr<FirstParentIsNarrowClass>>(module, "FirstParentIsNarrowClass")
        .def("child_function", &FirstParentIsNarrowClass::child_function)
        .def_property("child_property", py::overload_cast<>(&FirstParentIsNarrowClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsNarrowClass::set_child_property))
        ;
}

