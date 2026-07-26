

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/StructsQualifiedType.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Structs.h"
#include "smoke/StructsInstance.h"
#include "smoke/TypeCollection.h"
#include "memory"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using QualifiedType = ::fire::StructsQualifiedType::QualifiedType;

void register_fire_StructsQualifiedTypeQualifiedType(py::module_& module) {
    py::class_<QualifiedType>(module, "fire_StructsQualifiedTypeQualifiedType")
        .def_readwrite("type_collection_point", &QualifiedType::type_collection_point)
        .def_readwrite("interface_point", &QualifiedType::interface_point)
        .def_readwrite("type_collection_explicit_points", &QualifiedType::type_collection_explicit_points)
        .def_readwrite("interface_explicit_points", &QualifiedType::interface_explicit_points)
        .def_readwrite("type_collection_implicit_points", &QualifiedType::type_collection_implicit_points)
        .def_readwrite("interface_implicit_points", &QualifiedType::interface_implicit_points)
        .def_readwrite("structs_instance", &QualifiedType::structs_instance)
        .def(py::init<>())
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        ;
}

