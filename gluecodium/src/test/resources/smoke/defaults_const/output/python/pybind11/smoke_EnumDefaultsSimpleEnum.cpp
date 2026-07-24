

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum1.h"
#include "smoke/EnumDefaults.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SimpleEnum = ::smoke::EnumDefaults::SimpleEnum;

void register_smoke_EnumDefaultsSimpleEnum(py::module_& module) {
    py::class_<SimpleEnum>(module, "EnumDefaultsSimpleEnum")
        .def_readwrite("enum_field", &SimpleEnum::enum_field)
        .def(py::init<>())
        .def(py::init<::fire::Enum1(), py::arg("enum_field"))
        ;
}

