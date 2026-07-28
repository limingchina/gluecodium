

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerInternalClazz = ::smoke::OuterPublicClazz::InnerInternalClazz;


void register_smoke_OuterPublicClazzInnerInternalClazz(py::module_& module) {
    py::class_<InnerInternalClazz, std::shared_ptr<InnerInternalClazz>>(module, "smoke_OuterPublicClazzInnerInternalClazz")
        .def("__gluecodium_id__", [](const InnerInternalClazz& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_function", &InnerInternalClazz::some_function)
        ;
}

