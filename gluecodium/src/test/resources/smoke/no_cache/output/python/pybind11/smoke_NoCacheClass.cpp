

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
#include "smoke/NoCacheClass.h"
#include "memory"

using NoCacheClass = ::smoke::NoCacheClass;



void register_smoke_NoCacheClass(py::module_& module) {
auto cls_NoCacheClass = py::class_<NoCacheClass, std::shared_ptr<NoCacheClass>>(module, "smoke_NoCacheClass")
        .def("__gluecodium_id__", [](const NoCacheClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("make", &NoCacheClass::make)
        .def("foo", &NoCacheClass::foo)
        ;


}
