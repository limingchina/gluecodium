

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/StructWithJavaPositionalDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithJavaPositionalDefaults = ::gluecodium::smoke::StructWithJavaPositionalDefaults;

void register_StructWithJavaPositionalDefaults(py::module_& module) {
    py::class_<StructWithJavaPositionalDefaults>(module, "StructWithJavaPositionalDefaults")
        .def_readwrite("first_init_field", &StructWithJavaPositionalDefaults::first_init_field)
        .def_readwrite("first_free_field", &StructWithJavaPositionalDefaults::first_free_field)
        .def_readwrite("second_init_field", &StructWithJavaPositionalDefaults::second_init_field)
        .def_readwrite("second_free_field", &StructWithJavaPositionalDefaults::second_free_field)
        .def_readwrite("third_init_field", &StructWithJavaPositionalDefaults::third_init_field)
        .def(py::init<int32_t, ::std::string, float, bool, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"), py::arg("second_init_field"), py::arg("second_free_field"), py::arg("third_init_field"))
        ;
}

