

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/JavaInternalProperty.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaInternalProperty = ::smoke::JavaInternalProperty;


void register_JavaInternalProperty(py::module_& module) {
    py::class_<JavaInternalProperty, std::shared_ptr<JavaInternalProperty>>(module, "JavaInternalProperty")
        .def_property("app_context", py::overload_cast<>(&JavaInternalProperty::get_app_context, py::const_), py::overload_cast<const std::optional< ::std::string >&>(&JavaInternalProperty::set_app_context))
        ;
}

