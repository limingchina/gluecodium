

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
#include "smoke/KotlinInternalClass.h"

using KotlinInternalClass = ::smoke::KotlinInternalClass;



void register_smoke_KotlinInternalClass(py::module_& module) {
auto cls_KotlinInternalClass = py::class_<KotlinInternalClass, std::shared_ptr<KotlinInternalClass>>(module, "smoke_KotlinInternalClass")
        .def("__gluecodium_id__", [](const KotlinInternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
