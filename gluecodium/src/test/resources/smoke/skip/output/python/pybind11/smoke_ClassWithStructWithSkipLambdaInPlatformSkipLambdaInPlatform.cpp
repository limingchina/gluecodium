

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
#include "smoke/ClassWithStructWithSkipLambdaInPlatform.h"
#include "cstdint"
#include "functional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipLambdaInPlatform = ::smoke::ClassWithStructWithSkipLambdaInPlatform::SkipLambdaInPlatform;

void register_smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform(py::module_& module) {
    py::class_<SkipLambdaInPlatform>(module, "smoke_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform")
        .def_readwrite("int_field", &SkipLambdaInPlatform::int_field)
        .def_readwrite("some_lambda", &SkipLambdaInPlatform::some_lambda)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::function<int32_t()>>(), py::arg("int_field"), py::arg("some_lambda"))
        .def(py::init<int32_t, ::std::function<int32_t()>>(), py::arg("int_field"), py::arg("some_lambda"))
                .def("use_lambda", [](SkipLambdaInPlatform& self, const ::std::function<int32_t()>& some_lambda) -> py::object {
                        return py::cast(self.use_lambda(some_lambda));
                }, py::arg("some_lambda"))
        ;
}

