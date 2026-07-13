

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/LevelOne.h"
#include "smoke/OuterClass.h"
#include "smoke/OuterInterface.h"
#include "memory"
#include "string"

void register_LevelOne(py::module_& module) {
    py::class_<LevelOne>(module, "LevelOne")
        ;
}

