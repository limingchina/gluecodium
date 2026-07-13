

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Alphabet.h"
#include "smoke/LearnToRead.h"
#include "smoke/foo/Alphabet.h"

void register_LearnToRead(py::module_& module) {
    py::class_<LearnToRead>(module, "LearnToRead")
        .def_readwrite("field_a", &LearnToRead::field_a)
        .def_readwrite("field_b", &LearnToRead::field_b)
        ;
}

