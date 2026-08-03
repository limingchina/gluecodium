

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
#include "smoke/LambdaComments.h"
#include "functional"
#include "string"

using LambdaComments = ::smoke::LambdaComments;



void register_smoke_LambdaComments(py::module_& module) {
auto cls_LambdaComments = py::class_<LambdaComments, std::shared_ptr<LambdaComments>>(module, "smoke_LambdaComments")
        .def("__gluecodium_id__", [](const LambdaComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
