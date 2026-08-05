

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
#include "smoke/SwiftInternalClass.h"

using SwiftInternalClass = ::smoke::SwiftInternalClass;



void register_smoke_SwiftInternalClass(py::module_& module) {
auto cls_SwiftInternalClass = py::class_<SwiftInternalClass, std::shared_ptr<SwiftInternalClass>>(module, "smoke_SwiftInternalClass")
        .def("__gluecodium_id__", [](const SwiftInternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
