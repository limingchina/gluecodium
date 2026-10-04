

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
#include "include/ExternalTypes.h"
#include "cstdint"
#include "string"




void register_smoke_StructWithOverloads(py::module_& module) {
auto cls_StructWithOverloads = py::class_<external::ClassWithOverloads::StructWithOverloads>(module, "smoke_StructWithOverloads")
        .def_property("overloaded_accessors", static_cast<int32_t (external::ClassWithOverloads::StructWithOverloads::*)() const>(&external::ClassWithOverloads::StructWithOverloads::overloadedAccessors), py::overload_cast<const int32_t>(&external::ClassWithOverloads::StructWithOverloads::overloadedAccessors))
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("overloaded_accessors"))
        .def("overloaded_method", py::overload_cast<>(&external::ClassWithOverloads::StructWithOverloads::overloadedMethod))
        .def("overloaded_method", py::overload_cast<const ::std::string&>(&external::ClassWithOverloads::StructWithOverloads::overloadedMethod), py::arg("input"))
        .def("overloaded_method", py::overload_cast<const ::std::string&, const bool>(&external::ClassWithOverloads::StructWithOverloads::overloadedMethod), py::arg("input_string"), py::arg("input_bool"))
        ;


}
