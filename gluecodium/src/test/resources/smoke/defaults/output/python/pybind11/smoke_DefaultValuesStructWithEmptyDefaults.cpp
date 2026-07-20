

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
#include "cstdint"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithEmptyDefaults = ::smoke::DefaultValues::StructWithEmptyDefaults;

void register_DefaultValuesStructWithEmptyDefaults(py::module_& module) {
    py::class_<StructWithEmptyDefaults>(module, "DefaultValuesStructWithEmptyDefaults")
        .def_readwrite("ints_field", &StructWithEmptyDefaults::ints_field)
        .def_readwrite("floats_field", &StructWithEmptyDefaults::floats_field)
        .def_readwrite("map_field", &StructWithEmptyDefaults::map_field)
        .def_readwrite("struct_field", &StructWithEmptyDefaults::struct_field)
        .def_readwrite("set_type_field", &StructWithEmptyDefaults::set_type_field)
        .def(py::init<>())
        ;
}

