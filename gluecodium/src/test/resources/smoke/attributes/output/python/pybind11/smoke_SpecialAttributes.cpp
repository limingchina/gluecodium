

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SpecialAttributes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SpecialAttributes = ::gluecodium::smoke::SpecialAttributes;

void register_SpecialAttributes(py::module_& module) {
    py::class_<SpecialAttributes, std::shared_ptr<SpecialAttributes>>(module, "SpecialAttributes")
        .def("with_escaping", &SpecialAttributes::with_escaping)
        .def("with_line_break", &SpecialAttributes::with_line_break)
        ;
}

