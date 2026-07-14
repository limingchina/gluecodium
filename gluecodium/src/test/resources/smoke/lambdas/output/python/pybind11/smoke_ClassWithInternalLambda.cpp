

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ClassWithInternalLambda.h"
#include "functional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ClassWithInternalLambda = ::smoke::ClassWithInternalLambda;

void register_ClassWithInternalLambda(py::module_& module) {
    py::class_<ClassWithInternalLambda, std::shared_ptr<ClassWithInternalLambda>>(module, "ClassWithInternalLambda")
        .def_static("invoke_internal_lambda", &ClassWithInternalLambda::invoke_internal_lambda, py::arg("lambda"), py::arg("value"))
        ;
}

