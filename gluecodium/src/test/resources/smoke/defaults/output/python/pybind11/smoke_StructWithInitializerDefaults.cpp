

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "smoke/StructWithInitializerDefaults.h"
#include "cstdint"
#include "vector"

void register_StructWithInitializerDefaults(py::module_& module) {
    py::class_<StructWithInitializerDefaults>(module, "StructWithInitializerDefaults")
        .def_readwrite("ints_field", &StructWithInitializerDefaults::ints_field)
        .def_readwrite("floats_field", &StructWithInitializerDefaults::floats_field)
        .def_readwrite("set_type_field", &StructWithInitializerDefaults::set_type_field)
        .def_readwrite("map_field", &StructWithInitializerDefaults::map_field)
        ;
}

