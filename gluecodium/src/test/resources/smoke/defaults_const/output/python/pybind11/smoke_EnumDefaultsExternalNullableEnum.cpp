

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum2.h"
#include "smoke/EnumDefaultsExternal.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableEnum = ::smoke::EnumDefaultsExternal::NullableEnum;

void register_smoke_EnumDefaultsExternalNullableEnum(py::module_& module) {
    py::class_<NullableEnum>(module, "EnumDefaultsExternalNullableEnum")
        .def_readwrite("enum_field1", &NullableEnum::enum_field1)
        .def_readwrite("enum_field2", &NullableEnum::enum_field2)
        .def(py::init<>())
        .def(py::init<std::optional< foo::AlienEnum2 >, std::optional< foo::AlienEnum2 >(), py::arg("enum_field1"), py::arg("enum_field2"))
        ;
}

