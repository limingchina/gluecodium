

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
#include "smoke/forward/Class2.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Class2 = ::smoke::forward::Class2;


void register_smoke_forward_Class2(py::module_& module) {
    py::class_<Class2, std::shared_ptr<Class2>>(module, "smoke_forward_Class2")
        .def("__gluecodium_id__", [](const Class2& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

