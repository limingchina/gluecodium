

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/bar/Alphabet.h"

using Alphabet = ::smoke::bar::Alphabet;



void register_smoke_bar_Alphabet(py::module_& module) {
auto cls_Alphabet = py::enum_<Alphabet>(module, "smoke_bar_Alphabet")
        .value("ALEPH", Alphabet::ALEPH)
        .value("BEIT", Alphabet::BEIT)
        .value("GIMEL", Alphabet::GIMEL)
        ;


}
