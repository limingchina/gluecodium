

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
#include "smoke/StructWithJavaPositionalDefaults.h"
#include "cstdint"
#include "string"

using StructWithJavaPositionalDefaults = ::smoke::StructWithJavaPositionalDefaults;



void register_smoke_StructWithJavaPositionalDefaults(py::module_& module) {
auto cls_StructWithJavaPositionalDefaults = py::class_<StructWithJavaPositionalDefaults>(module, "smoke_StructWithJavaPositionalDefaults")
        .def_readwrite("first_init_field", &StructWithJavaPositionalDefaults::first_init_field)
        .def_readwrite("first_free_field", &StructWithJavaPositionalDefaults::first_free_field)
        .def_readwrite("second_init_field", &StructWithJavaPositionalDefaults::second_init_field)
        .def_readwrite("second_free_field", &StructWithJavaPositionalDefaults::second_free_field)
        .def_readwrite("third_init_field", &StructWithJavaPositionalDefaults::third_init_field)
        .def(py::init<>())
        .def(py::init<::std::string, bool>(), py::arg("first_free_field"), py::arg("second_free_field"))
        .def(py::init<int32_t, ::std::string, float, bool, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"), py::arg("second_init_field"), py::arg("second_free_field"), py::arg("third_init_field"))
        ;


}
