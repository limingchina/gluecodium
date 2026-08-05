

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
#include "smoke/ImmutableDefaultCtor.h"
#include "smoke/MutableStructImmutableFieldsDefault.h"
#include "cstdint"

using MutableStructImmutableFieldsDefault = ::smoke::MutableStructImmutableFieldsDefault;



void register_smoke_MutableStructImmutableFieldsDefault(py::module_& module) {
auto cls_MutableStructImmutableFieldsDefault = py::class_<MutableStructImmutableFieldsDefault>(module, "smoke_MutableStructImmutableFieldsDefault")
        .def_readwrite("struct_field", &MutableStructImmutableFieldsDefault::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFieldsDefault::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFieldsDefault::bool_field)
        .def(py::init<>())
        ;


}
