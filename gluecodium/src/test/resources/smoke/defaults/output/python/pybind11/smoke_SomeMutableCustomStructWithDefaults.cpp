

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/SomeMutableCustomStructWithDefaults.h"
#include "cstdint"
#include "string"
#include "vector"

void register_SomeMutableCustomStructWithDefaults(py::module_& module) {
    py::class_<SomeMutableCustomStructWithDefaults>(module, "SomeMutableCustomStructWithDefaults")
        .def_readwrite("int_field", &SomeMutableCustomStructWithDefaults::int_field)
        .def_readwrite("string_field", &SomeMutableCustomStructWithDefaults::string_field)
        .def_readwrite("list_field", &SomeMutableCustomStructWithDefaults::list_field)
        ;
}

