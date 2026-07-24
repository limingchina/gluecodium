

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/StructsWithMethodsInterface.h"
#include "smoke/ValidationUtils.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Vector3 = ::smoke::StructsWithMethodsInterface::Vector3;

void register_smoke_StructsWithMethodsInterfaceVector3(py::module_& module) {
    py::class_<Vector3>(module, "StructsWithMethodsInterfaceVector3")
        .def_readwrite("x", &Vector3::x)
        .def_readwrite("y", &Vector3::y)
        .def_readwrite("z", &Vector3::z)
        .def(py::init<>())
        .def(py::init<double, double, double(), py::arg("x"), py::arg("y"), py::arg("z"))
        .def(py::init<::std::string>(py::arg("input")))

        .def_static("create", py::overload_cast<const ::std::string&>(&Vector3::create), py::arg("input"))
        .def(py::init<::smoke::StructsWithMethodsInterface::Vector3>(py::arg("other")))

        .def_static("create", py::overload_cast<const ::smoke::StructsWithMethodsInterface::Vector3&>(&Vector3::create), py::arg("other"))
        ;
}

