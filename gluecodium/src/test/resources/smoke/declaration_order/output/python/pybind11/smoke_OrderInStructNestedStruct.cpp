

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
using NestedStruct = ::smoke::OrderInStruct::NestedStruct;

void register_smoke_OrderInStructNestedStruct(py::module_& module) {
    py::class_<NestedStruct>(module, "smoke_OrderInStructNestedStruct")
        .def_readwrite("some_field", &NestedStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;
}

