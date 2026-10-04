

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
#include "gluecodium/Optional.h"
#include "smoke/NullableOverloads.h"
#include "string"

using NullableOverloads = ::smoke::NullableOverloads;



void register_smoke_NullableOverloads(py::module_& module) {
auto cls_NullableOverloads = py::class_<NullableOverloads, std::shared_ptr<NullableOverloads>>(module, "smoke_NullableOverloads")
        .def("__gluecodium_id__", [](const NullableOverloads& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("foo", py::overload_cast<const ::std::string&>(&NullableOverloads::foo), py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("foo", py::overload_cast<const ::gluecodium::optional< ::std::string >&>(&NullableOverloads::foo), py::arg("input"), py::call_guard<py::gil_scoped_release>())
        ;


}
