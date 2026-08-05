

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
#include "smoke/ImmutableStructWithDefaults.h"
#include "smoke/PosDefaultStructWithFieldUsingImmutableStruct.h"

using PosDefaultStructWithFieldUsingImmutableStruct = ::smoke::PosDefaultStructWithFieldUsingImmutableStruct;



void register_smoke_PosDefaultStructWithFieldUsingImmutableStruct(py::module_& module) {
auto cls_PosDefaultStructWithFieldUsingImmutableStruct = py::class_<PosDefaultStructWithFieldUsingImmutableStruct>(module, "smoke_PosDefaultStructWithFieldUsingImmutableStruct")
        .def_readonly("some_field1", &PosDefaultStructWithFieldUsingImmutableStruct::some_field1)
        .def(py::init<>())
        .def(py::init<::smoke::ImmutableStructWithDefaults>(), py::arg("some_field1"))
        ;


}
