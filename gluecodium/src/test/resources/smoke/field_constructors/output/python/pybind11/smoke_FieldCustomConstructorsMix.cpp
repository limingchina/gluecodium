

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldCustomConstructorsMix.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldCustomConstructorsMix = ::gluecodium::smoke::FieldCustomConstructorsMix;

void register_FieldCustomConstructorsMix(py::module_& module) {
    py::class_<FieldCustomConstructorsMix>(module, "FieldCustomConstructorsMix")
        .def_readwrite("string_field", &FieldCustomConstructorsMix::string_field)
        .def_readwrite("int_field", &FieldCustomConstructorsMix::int_field)
        .def_readwrite("bool_field", &FieldCustomConstructorsMix::bool_field)
        .def(py::init<>())
        .def("create_me", &FieldCustomConstructorsMix::create_me, py::arg("int_value"), py::arg("dummy"))
        ;
}

