

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
#include "smoke/FieldCustomConstructorsMix.h"
#include "cstdint"
#include "string"

using FieldCustomConstructorsMix = ::smoke::FieldCustomConstructorsMix;



void register_smoke_FieldCustomConstructorsMix(py::module_& module) {
auto cls_FieldCustomConstructorsMix = py::class_<FieldCustomConstructorsMix>(module, "smoke_FieldCustomConstructorsMix")
        .def_readwrite("string_field", &FieldCustomConstructorsMix::string_field)
        .def_readwrite("int_field", &FieldCustomConstructorsMix::int_field)
        .def_readwrite("bool_field", &FieldCustomConstructorsMix::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        .def_static("create_me", &FieldCustomConstructorsMix::create_me, py::arg("int_value"), py::arg("dummy"))
        ;


}
