

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum4.h"
#include "smoke/EnumWrapper.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumWrapper = ::smoke::EnumWrapper;

void register_EnumWrapper(py::module_& module) {
    py::class_<EnumWrapper>(module, "EnumWrapper")
        .def_readwrite("enum_field", &EnumWrapper::enum_field)
        .def(py::init<::fire::Enum4>(), py::arg("enum_field"))
        ;
}

