

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
#include "smoke/LevelOne.h"
#include "smoke/OuterClass.h"
#include "smoke/OuterInterface.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LevelTwo = ::smoke::LevelOne::LevelTwo;


void register_smoke_LevelOneLevelTwo(py::module_& module) {
    py::class_<LevelTwo, std::shared_ptr<LevelTwo>>(module, "smoke_LevelOneLevelTwo")
        ;
}

