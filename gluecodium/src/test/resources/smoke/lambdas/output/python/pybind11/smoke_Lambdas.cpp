

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Lambdas.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Lambdas = ::gluecodium::smoke::Lambdas;

void register_Lambdas(py::module_& module) {
    py::class_<Lambdas, std::shared_ptr<Lambdas>>(module, "Lambdas")
        .def("deconfuse", &Lambdas::deconfuse, py::arg("value"), py::arg("confuser"))
        .def("fuse", &Lambdas::fuse, py::arg("items"), py::arg("callback"))
        ;
}

