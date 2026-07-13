

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Constructors.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Constructors = ::gluecodium::smoke::Constructors;

void register_Constructors(py::module_& module) {
    py::class_<Constructors>(module, "Constructors")
        .def("create", &Constructors::create)
        .def("create", &Constructors::create, py::arg("other"))
        .def("create", &Constructors::create, py::arg("foo"), py::arg("bar"))
        .def("create", &Constructors::create, py::arg("input"))
        .def("create", &Constructors::create, py::arg("input"))
        .def("create", &Constructors::create, py::arg("input"))
        ;
}

