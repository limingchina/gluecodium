

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
#include "fire/SomeStruct.h"
#include "cstdint"

using SomeStruct = ::fire::SomeStruct;



void register_fire_SomeStruct(py::module_& module) {
auto cls_SomeStruct = py::class_<SomeStruct>(module, "fire_SomeStruct")
        .def_readwrite("int_field", &SomeStruct::int_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        ;


}
