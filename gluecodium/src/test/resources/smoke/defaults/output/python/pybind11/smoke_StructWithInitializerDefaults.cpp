

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "smoke/StructWithInitializerDefaults.h"
#include "cstdint"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithInitializerDefaults = ::smoke::StructWithInitializerDefaults;

void register_StructWithInitializerDefaults(py::module_& module) {
    py::class_<StructWithInitializerDefaults>(module, "StructWithInitializerDefaults")
        .def_readwrite("ints_field", &StructWithInitializerDefaults::ints_field)
        .def_readwrite("floats_field", &StructWithInitializerDefaults::floats_field)
        .def_readwrite("set_type_field", &StructWithInitializerDefaults::set_type_field)
        .def_readwrite("map_field", &StructWithInitializerDefaults::map_field)
        .def(py::init<>())
        ;
}

