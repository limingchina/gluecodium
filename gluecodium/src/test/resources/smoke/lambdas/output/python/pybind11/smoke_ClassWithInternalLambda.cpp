

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
#include "smoke/ClassWithInternalLambda.h"
#include "functional"
#include "string"

using ClassWithInternalLambda = ::smoke::ClassWithInternalLambda;



void register_smoke_ClassWithInternalLambda(py::module_& module) {
auto cls_ClassWithInternalLambda = py::class_<ClassWithInternalLambda, std::shared_ptr<ClassWithInternalLambda>>(module, "smoke_ClassWithInternalLambda")
        .def("__gluecodium_id__", [](const ClassWithInternalLambda& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
                .def_static("invoke_internal_lambda", [](const ::std::function<bool(const ::std::string&)>& lambda_, const ::std::string& value) {
                        return ClassWithInternalLambda::invoke_internal_lambda(lambda_, value);
                }, py::arg("lambda_"), py::arg("value"))
        ;


}
