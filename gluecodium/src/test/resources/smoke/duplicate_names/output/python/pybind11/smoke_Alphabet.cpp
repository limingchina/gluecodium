

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Alphabet.h"

void register_Alphabet(py::module_& module) {
    py::enum_<Alphabet>(module, "Alphabet")
        .value("A", Alphabet::A)
        .value("B", Alphabet::B)
        .value("C", Alphabet::C)
        ;
}

