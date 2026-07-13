

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/SomeMutableCustomStructWithDefaults.h"
#include "cstdint"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeMutableCustomStructWithDefaults = ::gluecodium::smoke::SomeMutableCustomStructWithDefaults;

void register_SomeMutableCustomStructWithDefaults(py::module_& module) {
    py::class_<SomeMutableCustomStructWithDefaults>(module, "SomeMutableCustomStructWithDefaults")
        .def_readwrite("int_field", &SomeMutableCustomStructWithDefaults::int_field)
        .def_readwrite("string_field", &SomeMutableCustomStructWithDefaults::string_field)
        .def_readwrite("list_field", &SomeMutableCustomStructWithDefaults::list_field)
        ;
}

