

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/JavaInternalPropertyRev.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaInternalPropertyRev = ::smoke::JavaInternalPropertyRev;


void register_smoke_JavaInternalPropertyRev(py::module_& module) {
    py::class_<JavaInternalPropertyRev, std::shared_ptr<JavaInternalPropertyRev>>(module, "JavaInternalPropertyRev")
        .def_property("app_context", py::overload_cast<>(&JavaInternalPropertyRev::get_app_context, py::const_), py::overload_cast<const std::optional< ::std::string >&>(&JavaInternalPropertyRev::set_app_context))
        ;
}

