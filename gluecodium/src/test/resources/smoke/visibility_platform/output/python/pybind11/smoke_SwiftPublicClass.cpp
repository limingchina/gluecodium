

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
#include "smoke/SwiftPublicClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SwiftPublicClass = ::smoke::SwiftPublicClass;


void register_smoke_SwiftPublicClass(py::module_& module) {
    py::class_<SwiftPublicClass, std::shared_ptr<SwiftPublicClass>>(module, "smoke_SwiftPublicClass")
        .def("__gluecodium_id__", [](const SwiftPublicClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

