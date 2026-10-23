

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
#include "gluecodium/VectorHash.h"
#include "smoke/TypeCollection.h"
#include "smoke/TypeDefs.h"
#include "string"
#include "vector"

using TypeDefs = ::smoke::TypeDefs;
using StructHavingAliasFieldDefinedBelow = ::smoke::TypeDefs::StructHavingAliasFieldDefinedBelow;
using TestStruct = ::smoke::TypeDefs::TestStruct;



void register_smoke_TypeDefs(py::module_& module) {
auto cls_TypeDefs = py::class_<TypeDefs, std::shared_ptr<TypeDefs>>(module, "smoke_TypeDefs")
        .def("__gluecodium_id__", [](const TypeDefs& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("method_with_primitive_type_def", &TypeDefs::method_with_primitive_type_def, py::arg("input"), py::call_guard<py::gil_scoped_release>())
                .def_static("method_with_complex_type_def", [](const ::std::vector< ::smoke::TypeDefs::TestStruct >& input) -> py::object {
                        return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) { return TypeDefs::method_with_complex_type_def(input); }));
                }, py::arg("input"))
        .def_static("return_nested_int_type_def", &TypeDefs::return_nested_int_type_def, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("return_test_struct_type_def", &TypeDefs::return_test_struct_type_def, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("return_nested_struct_type_def", &TypeDefs::return_nested_struct_type_def, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("return_type_def_point_from_type_collection", &TypeDefs::return_type_def_point_from_type_collection, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_property("primitive_type_property", [](const TypeDefs& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_primitive_type_property();
            }));
        }, [](TypeDefs& self, const ::std::vector< double >& value) {
            gluecodium::python::call_native([&] {
                self.set_primitive_type_property(value);
            });
        })
        ;

auto cls_TypeDefsStructHavingAliasFieldDefinedBelow = py::class_<StructHavingAliasFieldDefinedBelow>(cls_TypeDefs, "StructHavingAliasFieldDefinedBelow")
        .def_property("field", [](const StructHavingAliasFieldDefinedBelow& self) -> decltype(auto) {
            return
                (self.field)
            ;
        }, [](StructHavingAliasFieldDefinedBelow& self, const double value) {

                self.field = value;

        })
        .def(py::init<>())
        .def(py::init<double>(), py::arg("field"))
        ;

auto cls_TypeDefsTestStruct = py::class_<TestStruct>(cls_TypeDefs, "TestStruct")
        .def_property("something", [](const TestStruct& self) -> decltype(auto) {
            return
                (self.something)
            ;
        }, [](TestStruct& self, const ::std::string& value) {

                self.something = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("something"))
        ;


}
