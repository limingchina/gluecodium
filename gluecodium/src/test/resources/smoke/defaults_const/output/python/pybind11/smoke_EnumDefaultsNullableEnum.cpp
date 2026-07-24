

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum2.h"
#include "smoke/EnumDefaults.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableEnum = ::smoke::EnumDefaults::NullableEnum;

void register_smoke_EnumDefaultsNullableEnum(py::module_& module) {
    py::class_<NullableEnum>(module, "EnumDefaultsNullableEnum")
        .def_readwrite("enum_field1", &NullableEnum::enum_field1)
        .def_readwrite("enum_field1", &NullableEnum::enum_field1)
        .def(py::init<>())
        .def(py::init<std::optional< ::fire::Enum2 >, std::optional< ::fire::Enum2 >(), py::arg("enum_field1"), py::arg("enum_field1"))
        ;
}

