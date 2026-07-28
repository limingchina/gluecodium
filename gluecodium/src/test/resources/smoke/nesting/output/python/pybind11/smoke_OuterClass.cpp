

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
#include "smoke/OuterClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterClass = ::smoke::OuterClass;


void register_smoke_OuterClass(py::module_& module) {
    py::class_<OuterClass, std::shared_ptr<OuterClass>>(module, "smoke_OuterClass")
        .def("__gluecodium_id__", [](const OuterClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("foo", &OuterClass::foo, py::arg("input"))
        ;
}

