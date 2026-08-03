

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
#include "smoke/SwiftInternalClassRev.h"

using SwiftInternalClassRev = ::smoke::SwiftInternalClassRev;



void register_smoke_SwiftInternalClassRev(py::module_& module) {
auto cls_SwiftInternalClassRev = py::class_<SwiftInternalClassRev, std::shared_ptr<SwiftInternalClassRev>>(module, "smoke_SwiftInternalClassRev")
        .def("__gluecodium_id__", [](const SwiftInternalClassRev& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
