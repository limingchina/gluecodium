

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
#include "smoke/Annotations.h"
#include "memory"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Annotations = ::smoke::Annotations;


void register_smoke_Annotations(py::module_& module) {
    py::class_<Annotations, std::shared_ptr<Annotations>>(module, "smoke_Annotations")
        .def("__gluecodium_id__", [](const Annotations& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("test_optional", &Annotations::test_optional, py::arg("self"))
        ;
}

