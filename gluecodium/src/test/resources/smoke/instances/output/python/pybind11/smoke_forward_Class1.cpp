

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
#include "smoke/forward/Class1.h"

using Class1 = ::smoke::forward::Class1;



void register_smoke_forward_Class1(py::module_& module) {
auto cls_Class1 = py::class_<Class1, std::shared_ptr<Class1>>(module, "smoke_forward_Class1")
        .def("__gluecodium_id__", [](const Class1& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
