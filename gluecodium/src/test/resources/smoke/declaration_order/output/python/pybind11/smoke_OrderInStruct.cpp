

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
#include "smoke/OrderInStruct.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OrderInStruct = ::smoke::OrderInStruct;

void register_smoke_OrderInStruct(py::module_& module) {
    py::class_<OrderInStruct>(module, "smoke_OrderInStruct")
        .def_readwrite("struct_field", &OrderInStruct::struct_field)
        .def_readwrite("enum_field", &OrderInStruct::enum_field)
        .def(py::init<>())
        .def(py::init<::smoke::OrderInStruct::NestedStruct, ::smoke::OrderInStruct::SomeEnum>(), py::arg("struct_field"), py::arg("enum_field"))
        .def(py::init<::smoke::OrderInStruct::NestedStruct, ::smoke::OrderInStruct::SomeEnum>(), py::arg("struct_field"), py::arg("enum_field"))
        ;
}

