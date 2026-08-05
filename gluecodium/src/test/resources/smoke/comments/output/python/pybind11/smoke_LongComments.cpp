

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/LongComments.h"
#include "string"

using LongComments = ::smoke::LongComments;



void register_smoke_LongComments(py::module_& module) {
auto cls_LongComments = py::class_<LongComments, std::shared_ptr<LongComments>>(module, "smoke_LongComments")
        .def("__gluecodium_id__", [](const LongComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_long_comment", &LongComments::some_method_with_long_comment, py::arg("input"), py::arg("ratio"))
        ;


}
