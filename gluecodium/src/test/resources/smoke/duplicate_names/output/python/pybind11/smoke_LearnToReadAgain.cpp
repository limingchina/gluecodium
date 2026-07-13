

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/LearnToReadAgain.h"
#include "smoke/bar/Alphabet.h"
#include "smoke/foo/Alphabet.h"

void register_LearnToReadAgain(py::module_& module) {
    py::class_<LearnToReadAgain>(module, "LearnToReadAgain")
        .def_readwrite("field_b", &LearnToReadAgain::field_b)
        .def_readwrite("field_c", &LearnToReadAgain::field_c)
        ;
}

