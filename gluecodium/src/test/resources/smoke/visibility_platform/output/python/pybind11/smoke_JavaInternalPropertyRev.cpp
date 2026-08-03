

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
#include "smoke/JavaInternalPropertyRev.h"
#include "optional"
#include "string"

using JavaInternalPropertyRev = ::smoke::JavaInternalPropertyRev;



void register_smoke_JavaInternalPropertyRev(py::module_& module) {
auto cls_JavaInternalPropertyRev = py::class_<JavaInternalPropertyRev, std::shared_ptr<JavaInternalPropertyRev>>(module, "smoke_JavaInternalPropertyRev")
        .def("__gluecodium_id__", [](const JavaInternalPropertyRev& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_property("app_context", py::overload_cast<>(&JavaInternalPropertyRev::get_app_context, py::const_), py::overload_cast<const std::optional< ::std::string >&>(&JavaInternalPropertyRev::set_app_context))
        ;


}
