

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
#include "smoke/DefaultValues.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithTypedefDefaults = ::smoke::DefaultValues::StructWithTypedefDefaults;

void register_smoke_DefaultValuesStructWithTypedefDefaults(py::module_& module) {
    py::class_<StructWithTypedefDefaults>(module, "smoke_DefaultValuesStructWithTypedefDefaults")
        .def_readwrite("long_field", &StructWithTypedefDefaults::long_field)
        .def_readwrite("bool_field", &StructWithTypedefDefaults::bool_field)
        .def_readwrite("string_field", &StructWithTypedefDefaults::string_field)
        .def(py::init<>())
        .def(py::init<int64_t, bool, ::std::string>(), py::arg("long_field"), py::arg("bool_field"), py::arg("string_field"))
        ;
}

