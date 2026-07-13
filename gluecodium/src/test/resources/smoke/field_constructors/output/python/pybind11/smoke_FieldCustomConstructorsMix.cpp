

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldCustomConstructorsMix.h"
#include "cstdint"
#include "string"

void register_FieldCustomConstructorsMix(py::module_& module) {
    py::class_<FieldCustomConstructorsMix>(module, "FieldCustomConstructorsMix")
        .def_readwrite("string_field", &FieldCustomConstructorsMix::string_field)
        .def_readwrite("int_field", &FieldCustomConstructorsMix::int_field)
        .def_readwrite("bool_field", &FieldCustomConstructorsMix::bool_field)
        .def("create_me", &FieldCustomConstructorsMix::create_me, py::arg("int_value"), py::arg("dummy"))
        ;
}

