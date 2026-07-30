

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
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableStructWithDefaults = ::smoke::DefaultValues::NullableStructWithDefaults;

void register_smoke_DefaultValuesNullableStructWithDefaults(py::module_& module) {
    py::class_<NullableStructWithDefaults>(module, "smoke_DefaultValuesNullableStructWithDefaults")
        .def_readwrite("int_field", &NullableStructWithDefaults::int_field)
        .def_readwrite("uint_field", &NullableStructWithDefaults::uint_field)
        .def_readwrite("float_field", &NullableStructWithDefaults::float_field)
        .def_readwrite("bool_field", &NullableStructWithDefaults::bool_field)
        .def_readwrite("string_field", &NullableStructWithDefaults::string_field)
        .def(py::init<>())
        .def(py::init<std::optional< int32_t >, std::optional< uint32_t >, std::optional< float >, std::optional< bool >, std::optional< ::std::string >>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("bool_field"), py::arg("string_field"))
        ;
}

