

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
#include "smoke/SomeInterface.h"

using SomeInterface = ::smoke::SomeInterface;



void register_smoke_SomeInterface(py::module_& module) {
auto cls_SomeInterface = py::class_<SomeInterface, std::shared_ptr<SomeInterface>>(module, "smoke_SomeInterface")
        .def("__gluecodium_id__", [](const SomeInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
