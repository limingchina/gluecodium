

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/KotlinMethodOverloads.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using KotlinMethodOverloads = ::gluecodium::smoke::KotlinMethodOverloads;

void register_KotlinMethodOverloads(py::module_& module) {
    py::class_<KotlinMethodOverloads, std::shared_ptr<KotlinMethodOverloads>>(module, "KotlinMethodOverloads")
        .def("one", &KotlinMethodOverloads::one, py::arg("input"))
        .def("two", &KotlinMethodOverloads::two, py::arg("input"))
        ;
}

