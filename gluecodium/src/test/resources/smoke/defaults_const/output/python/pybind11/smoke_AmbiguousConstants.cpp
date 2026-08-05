

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
#include "smoke/AmbiguousConstants.h"

using AmbiguousConstants = ::smoke::AmbiguousConstants;



void register_smoke_AmbiguousConstants(py::module_& module) {
auto cls_AmbiguousConstants = py::class_<AmbiguousConstants, std::shared_ptr<AmbiguousConstants>>(module, "smoke_AmbiguousConstants")
        .def("__gluecodium_id__", [](const AmbiguousConstants& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
