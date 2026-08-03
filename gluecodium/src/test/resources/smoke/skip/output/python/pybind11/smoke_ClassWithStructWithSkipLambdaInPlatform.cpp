

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

using ClassWithStructWithSkipLambdaInPlatform = ::smoke::ClassWithStructWithSkipLambdaInPlatform;
using SkipLambdaInPlatform = ::smoke::ClassWithStructWithSkipLambdaInPlatform::SkipLambdaInPlatform;



void register_smoke_ClassWithStructWithSkipLambdaInPlatform(py::module_& module) {
auto cls_ClassWithStructWithSkipLambdaInPlatform = py::class_<ClassWithStructWithSkipLambdaInPlatform, std::shared_ptr<ClassWithStructWithSkipLambdaInPlatform>>(module, "smoke_ClassWithStructWithSkipLambdaInPlatform")
        .def("__gluecodium_id__", [](const ClassWithStructWithSkipLambdaInPlatform& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_ClassWithStructWithSkipLambdaInPlatformSkipLambdaInPlatform = py::class_<SkipLambdaInPlatform>(cls_ClassWithStructWithSkipLambdaInPlatform, "SkipLambdaInPlatform")
        .def_readwrite("int_field", &SkipLambdaInPlatform::int_field)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::function<int32_t()>>(), py::arg("int_field"), py::arg("some_lambda"))
        ;


}
