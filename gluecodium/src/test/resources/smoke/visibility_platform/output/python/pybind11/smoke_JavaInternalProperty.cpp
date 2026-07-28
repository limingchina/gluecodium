

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
#include "smoke/JavaInternalProperty.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaInternalProperty = ::smoke::JavaInternalProperty;


void register_smoke_JavaInternalProperty(py::module_& module) {
    py::class_<JavaInternalProperty, std::shared_ptr<JavaInternalProperty>>(module, "smoke_JavaInternalProperty")
        .def("__gluecodium_id__", [](const JavaInternalProperty& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_property("app_context", py::overload_cast<>(&JavaInternalProperty::get_app_context, py::const_), py::overload_cast<const std::optional< ::std::string >&>(&JavaInternalProperty::set_app_context))
        ;
}

