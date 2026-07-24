

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DeclarationOrder.h"
#include "cstdint"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MainStruct = ::smoke::DeclarationOrder::MainStruct;

void register_smoke_DeclarationOrderMainStruct(py::module_& module) {
    py::class_<MainStruct>(module, "DeclarationOrderMainStruct")
        .def_readwrite("struct_field", &MainStruct::struct_field)
        .def_readwrite("type_def_field", &MainStruct::type_def_field)
        .def_readwrite("struct_array_field", &MainStruct::struct_array_field)
        .def_readwrite("map_field", &MainStruct::map_field)
        .def_readwrite("enum_field", &MainStruct::enum_field)
        .def(py::init<>())
        .def(py::init<::smoke::DeclarationOrder::NestedStruct, int32_t, ::std::vector< ::smoke::DeclarationOrder::NestedStruct >, ::std::unordered_map< int32_t, ::std::vector< ::smoke::DeclarationOrder::NestedStruct > >, ::smoke::DeclarationOrder::SomeEnum(), py::arg("struct_field"), py::arg("type_def_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("enum_field"))
        ;
}

