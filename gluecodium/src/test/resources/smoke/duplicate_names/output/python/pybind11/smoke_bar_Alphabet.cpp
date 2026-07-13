

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/bar/Alphabet.h"

void register_Alphabet(py::module_& module) {
    py::enum_<Alphabet>(module, "Alphabet")
        .value("ALEPH", Alphabet::ALEPH)
        .value("BEIT", Alphabet::BEIT)
        .value("GIMEL", Alphabet::GIMEL)
        ;
}

