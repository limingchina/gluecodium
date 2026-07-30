

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
#include "smoke/Alphabet.h"
#include "smoke/LearnToRead.h"
#include "smoke/foo/Alphabet.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LearnToRead = ::smoke::LearnToRead;

void register_smoke_LearnToRead(py::module_& module) {
    py::class_<LearnToRead>(module, "smoke_LearnToRead")
        .def_readwrite("field_a", &LearnToRead::field_a)
        .def_readwrite("field_b", &LearnToRead::field_b)
        .def(py::init<>())
        .def(py::init<::smoke::Alphabet, ::smoke::foo::Alphabet>(), py::arg("field_a"), py::arg("field_b"))
        ;
}

