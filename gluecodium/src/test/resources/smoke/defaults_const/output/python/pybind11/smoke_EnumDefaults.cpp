

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum1.h"
#include "fire/Enum2.h"
#include "smoke/EnumDefaults.h"
#include "smoke/EnumWrapper.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumDefaults = ::smoke::EnumDefaults;

void register_EnumDefaults(py::module_& module) {
    py::class_<EnumDefaults, std::shared_ptr<EnumDefaults>>(module, "EnumDefaults")
        ;
}

