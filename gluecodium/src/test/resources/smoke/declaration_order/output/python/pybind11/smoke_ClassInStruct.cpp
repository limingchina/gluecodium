

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ClassInStruct.h"
#include "functional"
#include "memory"

void register_ClassInStruct(py::module_& module) {
    py::class_<ClassInStruct>(module, "ClassInStruct")
        ;
}

