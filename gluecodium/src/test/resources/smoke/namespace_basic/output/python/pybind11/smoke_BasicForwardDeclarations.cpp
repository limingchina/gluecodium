

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "root/space/smoke/Basic.h"
#include "root/space/smoke/BasicForwardDeclarations.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using BasicForwardDeclarations = ::root::space::smoke::BasicForwardDeclarations;


void register_BasicForwardDeclarations(py::module_& module) {
    py::class_<BasicForwardDeclarations, std::shared_ptr<BasicForwardDeclarations>>(module, "BasicForwardDeclarations")
        .def("use_basic", &BasicForwardDeclarations::use_basic)

        ;
}

