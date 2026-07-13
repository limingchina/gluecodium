

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/foo/Alphabet.h"

void register_Alphabet(py::module_& module) {
    py::enum_<Alphabet>(module, "Alphabet")
        .value("ALPHA", Alphabet::ALPHA)
        .value("BETA", Alphabet::BETA)
        .value("GAMMA", Alphabet::GAMMA)
        ;
}

