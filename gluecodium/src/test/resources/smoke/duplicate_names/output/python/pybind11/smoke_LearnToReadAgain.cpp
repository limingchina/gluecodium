

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/LearnToReadAgain.h"
#include "smoke/bar/Alphabet.h"
#include "smoke/foo/Alphabet.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LearnToReadAgain = ::gluecodium::smoke::LearnToReadAgain;

void register_LearnToReadAgain(py::module_& module) {
    py::class_<LearnToReadAgain>(module, "LearnToReadAgain")
        .def_readwrite("field_b", &LearnToReadAgain::field_b)
        .def_readwrite("field_c", &LearnToReadAgain::field_c)
        .def(py::init<>())
        .def(py::init<::smoke::foo::Alphabet, ::smoke::bar::Alphabet>(), py::arg("field_b"), py::arg("field_c"))
        ;
}

