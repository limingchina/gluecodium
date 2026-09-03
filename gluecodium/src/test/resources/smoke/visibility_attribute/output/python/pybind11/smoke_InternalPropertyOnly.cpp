

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalPropertyOnly.h"
#include "string"

using InternalPropertyOnly = ::smoke::InternalPropertyOnly;



void register_smoke_InternalPropertyOnly(py::module_& module) {
auto cls_InternalPropertyOnly = py::class_<InternalPropertyOnly, std::shared_ptr<InternalPropertyOnly>>(module, "smoke_InternalPropertyOnly")
        .def("__gluecodium_id__", [](const InternalPropertyOnly& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_property("_foo", py::overload_cast<>(&InternalPropertyOnly::get_foo, py::const_), py::overload_cast<const ::std::string&>(&InternalPropertyOnly::set_foo))
        ;


}
