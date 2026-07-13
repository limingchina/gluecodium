

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SingleNamedConstructor.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SingleNamedConstructor = ::smoke::SingleNamedConstructor;

void register_SingleNamedConstructor(py::module_& module) {
    py::class_<SingleNamedConstructor, std::shared_ptr<SingleNamedConstructor>>(module, "SingleNamedConstructor")
        .def("create", &SingleNamedConstructor::create)
        ;
}

