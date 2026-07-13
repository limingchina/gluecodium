

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "package/Types.h"

void register_Types(py::module_& module) {
    py::class_<Types>(module, "Types")
        ;
}

