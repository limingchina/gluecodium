

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ClassWithInternalLambda.h"
#include "functional"
#include "string"

void register_ClassWithInternalLambda(py::module_& module) {
    py::class_<ClassWithInternalLambda>(module, "ClassWithInternalLambda")
        .def("invoke_internal_lambda", &ClassWithInternalLambda::invoke_internal_lambda, py::arg("lambda"), py::arg("value"))
        ;
}

