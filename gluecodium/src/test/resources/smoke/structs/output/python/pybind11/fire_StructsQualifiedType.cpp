

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/StructsQualifiedType.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Structs.h"
#include "smoke/StructsInstance.h"
#include "smoke/TypeCollection.h"
#include "memory"
#include "vector"

using StructsQualifiedType = ::fire::StructsQualifiedType;
using QualifiedType = ::fire::StructsQualifiedType::QualifiedType;



void register_fire_StructsQualifiedType(py::module_& module) {
auto cls_StructsQualifiedType = py::class_<StructsQualifiedType, std::shared_ptr<StructsQualifiedType>>(module, "fire_StructsQualifiedType")
        .def("__gluecodium_id__", [](const StructsQualifiedType& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_StructsQualifiedTypeQualifiedType = py::class_<QualifiedType>(cls_StructsQualifiedType, "QualifiedType")
        .def_property("type_collection_point", [](const QualifiedType& self) -> decltype(auto) {
            return
                (self.type_collection_point)
            ;
        }, [](QualifiedType& self, const ::smoke::TypeCollection::Point& value) {

                self.type_collection_point = value;

        })
        .def_property("interface_point", [](const QualifiedType& self) -> decltype(auto) {
            return
                (self.interface_point)
            ;
        }, [](QualifiedType& self, const ::smoke::Structs::Point& value) {

                self.interface_point = value;

        })
        .def_property("type_collection_explicit_points", [](const QualifiedType& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.type_collection_explicit_points)
            );
        }, [](QualifiedType& self, const ::std::vector< ::smoke::Structs::Point >& value) {

                self.type_collection_explicit_points = value;

        })
        .def_property("interface_explicit_points", [](const QualifiedType& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.interface_explicit_points)
            );
        }, [](QualifiedType& self, const ::std::vector< ::smoke::Structs::Point >& value) {

                self.interface_explicit_points = value;

        })
        .def_property("type_collection_implicit_points", [](const QualifiedType& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.type_collection_implicit_points)
            );
        }, [](QualifiedType& self, const ::std::vector< ::smoke::TypeCollection::Point >& value) {

                self.type_collection_implicit_points = value;

        })
        .def_property("interface_implicit_points", [](const QualifiedType& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.interface_implicit_points)
            );
        }, [](QualifiedType& self, const ::std::vector< ::smoke::Structs::Point >& value) {

                self.interface_implicit_points = value;

        })
        .def_property("structs_instance", [](const QualifiedType& self) -> decltype(auto) {
            return
                (self.structs_instance)
            ;
        }, [](QualifiedType& self, const ::std::shared_ptr< ::smoke::StructsInstance >& value) {

                self.structs_instance = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::Structs::Point, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::vector< ::smoke::TypeCollection::Point >, ::std::vector< ::smoke::Structs::Point >, ::std::shared_ptr< ::smoke::StructsInstance >>(), py::arg("type_collection_point"), py::arg("interface_point"), py::arg("type_collection_explicit_points"), py::arg("interface_explicit_points"), py::arg("type_collection_implicit_points"), py::arg("interface_implicit_points"), py::arg("structs_instance"))
        ;


}
