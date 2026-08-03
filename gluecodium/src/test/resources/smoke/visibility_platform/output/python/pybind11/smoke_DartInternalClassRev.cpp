

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
#include "smoke/DartInternalClassRev.h"

using DartInternalClassRev = ::smoke::DartInternalClassRev;



void register_smoke_DartInternalClassRev(py::module_& module) {
auto cls_DartInternalClassRev = py::class_<DartInternalClassRev, std::shared_ptr<DartInternalClassRev>>(module, "smoke_DartInternalClassRev")
        .def("__gluecodium_id__", [](const DartInternalClassRev& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
