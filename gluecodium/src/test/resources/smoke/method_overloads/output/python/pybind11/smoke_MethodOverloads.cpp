

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
#include "gluecodium/VectorHash.h"
#include "smoke/MethodOverloads.h"
#include "cstdint"
#include "string"
#include "vector"

using MethodOverloads = ::smoke::MethodOverloads;
using Point = ::smoke::MethodOverloads::Point;



void register_smoke_MethodOverloads(py::module_& module) {
auto cls_MethodOverloads = py::class_<MethodOverloads, std::shared_ptr<MethodOverloads>>(module, "smoke_MethodOverloads")
        .def("__gluecodium_id__", [](const MethodOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("is_boolean", py::overload_cast<const bool>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const int8_t>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const ::std::string&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const ::smoke::MethodOverloads::Point&>(&MethodOverloads::is_boolean), py::arg("input"))
        .def("is_boolean", py::overload_cast<const bool, const int8_t, const ::std::string&, const ::smoke::MethodOverloads::Point&>(&MethodOverloads::is_boolean), py::arg("input1"), py::arg("input2"), py::arg("input3"), py::arg("input4"))
                .def("is_boolean", [](MethodOverloads& self, const ::std::vector< ::std::string >& input) {
                        return self.is_boolean(input);
                }, py::arg("input"))
                .def("is_boolean", [](MethodOverloads& self, const ::std::vector< int8_t >& input) {
                        return self.is_boolean(input);
                }, py::arg("input"))
        .def("is_boolean", py::overload_cast<>(&MethodOverloads::is_boolean))
        .def("is_float", py::overload_cast<const ::std::string&>(&MethodOverloads::is_float), py::arg("input"))
                .def("is_float", [](MethodOverloads& self, const ::std::vector< int8_t >& input) {
                        return self.is_float(input);
                }, py::arg("input"))
        ;

auto cls_MethodOverloadsPoint = py::class_<Point>(cls_MethodOverloads, "Point")
        .def_readwrite("x", &Point::x)
        .def_readwrite("y", &Point::y)
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        ;


}
