

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Locale.h"
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OuterStruct.h"
#include "chrono"
#include "cstdint"
#include "functional"
#include "memory"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

void register_OuterStruct(py::module_& module) {
    py::class_<OuterStruct>(module, "OuterStruct")
        .def_readwrite("field", &OuterStruct::field)
        .def("do_nothing", &OuterStruct::do_nothing)
        ;
}

