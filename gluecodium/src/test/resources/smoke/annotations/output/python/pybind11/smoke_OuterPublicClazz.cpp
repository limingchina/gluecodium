

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
#include "smoke/OuterPublicClazz.h"

using OuterPublicClazz = ::smoke::OuterPublicClazz;
using InnerInternalClazz = ::smoke::OuterPublicClazz::InnerInternalClazz;



void register_smoke_OuterPublicClazz(py::module_& module) {
auto cls_OuterPublicClazz = py::class_<OuterPublicClazz, std::shared_ptr<OuterPublicClazz>>(module, "smoke_OuterPublicClazz")
        .def("__gluecodium_id__", [](const OuterPublicClazz& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls__OuterPublicClazzInnerInternalClazz = py::class_<InnerInternalClazz, std::shared_ptr<InnerInternalClazz>>(cls_OuterPublicClazz, "_InnerInternalClazz")
        .def("__gluecodium_id__", [](const InnerInternalClazz& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_function", &InnerInternalClazz::some_function)
        ;


}
