

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CompressionState.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalGenerics.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

void register_UseDartExternalGenerics(py::module_& module) {
    py::class_<UseDartExternalGenerics>(module, "UseDartExternalGenerics")
        .def("use_generics", &UseDartExternalGenerics::use_generics, py::arg("list"), py::arg("set"))
        ;
}

