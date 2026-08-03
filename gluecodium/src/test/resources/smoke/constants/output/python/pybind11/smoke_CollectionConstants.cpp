

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
#include "smoke/CollectionConstants.h"

using CollectionConstants = ::smoke::CollectionConstants;



void register_smoke_CollectionConstants(py::module_& module) {
auto cls_CollectionConstants = py::class_<CollectionConstants, std::shared_ptr<CollectionConstants>>(module, "smoke_CollectionConstants")
        .def("__gluecodium_id__", [](const CollectionConstants& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
