

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ClassWithDocRef.h"

void register_ClassWithDocRef(py::module_& module) {
    py::class_<ClassWithDocRef>(module, "ClassWithDocRef")
        ;
}

