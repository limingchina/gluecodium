

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructsWithMethods.h"
#include "smoke/ValidationUtils.h"
#include "cstdint"

void register_StructsWithMethods(py::module_& module) {
    py::class_<StructsWithMethods>(module, "StructsWithMethods")
        ;
}

