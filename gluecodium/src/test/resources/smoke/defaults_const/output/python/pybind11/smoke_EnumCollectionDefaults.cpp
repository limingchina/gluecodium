

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum1.h"
#include "fire/Enum2.h"
#include "fire/Enum3.h"
#include "fire/Enum4.h"
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/EnumCollectionDefaults.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

void register_EnumCollectionDefaults(py::module_& module) {
    py::class_<EnumCollectionDefaults>(module, "EnumCollectionDefaults")
        .def_readwrite("list_field", &EnumCollectionDefaults::list_field)
        .def_readwrite("set_field", &EnumCollectionDefaults::set_field)
        .def_readwrite("map_field", &EnumCollectionDefaults::map_field)
        ;
}

