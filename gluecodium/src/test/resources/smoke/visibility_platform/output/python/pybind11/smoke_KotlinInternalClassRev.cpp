

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
#include "smoke/KotlinInternalClassRev.h"

using KotlinInternalClassRev = ::smoke::KotlinInternalClassRev;



void register_smoke_KotlinInternalClassRev(py::module_& module) {
auto cls_KotlinInternalClassRev = py::class_<KotlinInternalClassRev, std::shared_ptr<KotlinInternalClassRev>>(module, "smoke_KotlinInternalClassRev")
        .def("__gluecodium_id__", [](const KotlinInternalClassRev& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
