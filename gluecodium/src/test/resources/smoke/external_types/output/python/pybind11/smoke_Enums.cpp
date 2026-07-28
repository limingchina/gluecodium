

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
#include "foo/Bar.h"
#include "smoke/Enums.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Enums = ::smoke::Enums;


void register_smoke_Enums(py::module_& module) {
    py::class_<Enums, std::shared_ptr<Enums>>(module, "smoke_Enums")
        .def("__gluecodium_id__", [](const Enums& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("method_with_external_enum", &Enums::method_with_external_enum, py::arg("input"))
        ;
}

