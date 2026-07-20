

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/JavaMethodOverloads.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaMethodOverloads = ::smoke::JavaMethodOverloads;


void register_JavaMethodOverloads(py::module_& module) {
    py::class_<JavaMethodOverloads, std::shared_ptr<JavaMethodOverloads>>(module, "JavaMethodOverloads")
        .def("one", &JavaMethodOverloads::one, py::arg("input"))

        .def("two", &JavaMethodOverloads::two, py::arg("input"))

        ;
}

