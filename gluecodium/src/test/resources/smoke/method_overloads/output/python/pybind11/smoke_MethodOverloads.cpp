

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MethodOverloads.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MethodOverloads = ::smoke::MethodOverloads;

void register_MethodOverloads(py::module_& module) {
    py::class_<MethodOverloads, std::shared_ptr<MethodOverloads>>(module, "MethodOverloads")
        .def("is_boolean", py::overload_cast<const bool>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const int8_t>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const ::std::string&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const ::smoke::MethodOverloads::Point&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const bool, const int8_t, const ::std::string&, const ::smoke::MethodOverloads::Point&>(&MethodOverloads::is_boolean), py::arg("input1"), py::arg("input2"), py::arg("input3"), py::arg("input4"))
        .def("is_boolean", py::overload_cast<const ::std::vector< ::std::string >&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const ::std::vector< int8_t >&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<>(&MethodOverloads::is_boolean))
        .def("is_float", py::overload_cast<const ::std::string&>(&MethodOverloads::is_float), py::arg("input"))
        .def("is_float", py::overload_cast<const ::std::vector< int8_t >&>(&MethodOverloads::is_float), py::arg("input"))
        ;
}

