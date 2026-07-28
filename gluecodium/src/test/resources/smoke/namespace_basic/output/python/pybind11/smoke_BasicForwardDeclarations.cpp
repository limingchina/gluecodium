

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
#include "root/space/smoke/Basic.h"
#include "root/space/smoke/BasicForwardDeclarations.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using BasicForwardDeclarations = ::root::space::smoke::BasicForwardDeclarations;


void register_smoke_BasicForwardDeclarations(py::module_& module) {
    py::class_<BasicForwardDeclarations, std::shared_ptr<BasicForwardDeclarations>>(module, "smoke_BasicForwardDeclarations")
        .def("__gluecodium_id__", [](const BasicForwardDeclarations& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("use_basic", &BasicForwardDeclarations::use_basic)
        ;
}

