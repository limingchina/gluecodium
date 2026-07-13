

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "another/SomeCoolClassType.h"
#include "smoke/FirstParentIsInterfaceClass.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsInterfaceClass = ::smoke::FirstParentIsInterfaceClass;

void register_FirstParentIsInterfaceClass(py::module_& module) {
    py::class_<FirstParentIsInterfaceClass, std::shared_ptr<FirstParentIsInterfaceClass>>(module, "FirstParentIsInterfaceClass")
        .def("child_function", &FirstParentIsInterfaceClass::child_function)
        .def_property("child_property", py::overload_cast<>(&FirstParentIsInterfaceClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsInterfaceClass::set_child_property))
        ;
}

