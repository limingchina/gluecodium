

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
#include "smoke/SpecialNames.h"
#include "memory"
#include "string"

using SpecialNames = ::smoke::SpecialNames;



void register_smoke_SpecialNames(py::module_& module) {
auto cls_SpecialNames = py::class_<SpecialNames, std::shared_ptr<SpecialNames>>(module, "smoke_SpecialNames")
        .def("__gluecodium_id__", [](const SpecialNames& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("create", &SpecialNames::create, py::call_guard<py::gil_scoped_release>())
        .def("release", &SpecialNames::release, py::call_guard<py::gil_scoped_release>())
        .def("create_proxy", &SpecialNames::create_proxy, py::call_guard<py::gil_scoped_release>())
        .def("_uppercase", &SpecialNames::_uppercase, py::call_guard<py::gil_scoped_release>())
        .def_static("make", &SpecialNames::make, py::arg("result"), py::call_guard<py::gil_scoped_release>())
        ;


}
