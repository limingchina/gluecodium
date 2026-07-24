

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumDefaults.h"
#include "smoke/EnumWrapper.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using WrappedEnum = ::smoke::EnumDefaults::WrappedEnum;

void register_smoke_EnumDefaultsWrappedEnum(py::module_& module) {
    py::class_<WrappedEnum>(module, "EnumDefaultsWrappedEnum")
        .def_readwrite("struct_field", &WrappedEnum::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::EnumWrapper(), py::arg("struct_field"))
        ;
}

