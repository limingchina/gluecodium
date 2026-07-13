

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Serialization.h"
#include "cstdint"
#include "memory"
#include "string"
#include "unordered_set"
#include "vector"

void register_Serialization(py::module_& module) {
    py::class_<Serialization>(module, "Serialization")
        ;
}

