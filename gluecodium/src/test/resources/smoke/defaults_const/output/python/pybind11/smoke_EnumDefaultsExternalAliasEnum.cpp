

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum3.h"
#include "smoke/EnumDefaultsExternal.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AliasEnum = ::smoke::EnumDefaultsExternal::AliasEnum;

void register_smoke_EnumDefaultsExternalAliasEnum(py::module_& module) {
    py::class_<AliasEnum>(module, "EnumDefaultsExternalAliasEnum")
        .def_readwrite("enum_field", &AliasEnum::enum_field)
        .def(py::init<>())
        .def(py::init<foo::AlienEnum3(), py::arg("enum_field"))
        ;
}

