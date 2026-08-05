

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
#include "smoke/DartInternalClass.h"

using DartInternalClass = ::smoke::DartInternalClass;



void register_smoke_DartInternalClass(py::module_& module) {
auto cls_DartInternalClass = py::class_<DartInternalClass, std::shared_ptr<DartInternalClass>>(module, "smoke_DartInternalClass")
        .def("__gluecodium_id__", [](const DartInternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
