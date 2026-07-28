

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
#include "smoke/ConstantsInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ConstantsInterface = ::smoke::ConstantsInterface;


void register_smoke_ConstantsInterface(py::module_& module) {
    py::class_<ConstantsInterface, std::shared_ptr<ConstantsInterface>>(module, "smoke_ConstantsInterface")
        .def("__gluecodium_id__", [](const ConstantsInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

