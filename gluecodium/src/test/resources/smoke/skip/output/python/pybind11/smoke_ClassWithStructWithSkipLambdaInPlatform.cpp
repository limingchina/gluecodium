

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ClassWithStructWithSkipLambdaInPlatform.h"
#include "cstdint"
#include "functional"

void register_ClassWithStructWithSkipLambdaInPlatform(py::module_& module) {
    py::class_<ClassWithStructWithSkipLambdaInPlatform>(module, "ClassWithStructWithSkipLambdaInPlatform")
        ;
}

