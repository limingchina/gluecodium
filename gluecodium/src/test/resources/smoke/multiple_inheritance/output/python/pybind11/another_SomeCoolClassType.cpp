

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "another/SomeCoolClassType.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeCoolClassType = ::another::SomeCoolClassType;


void register_another_SomeCoolClassType(py::module_& module) {
    py::class_<SomeCoolClassType, std::shared_ptr<SomeCoolClassType>>(module, "SomeCoolClassType")
        ;
}

