

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
#include "gluecodium/VectorHash.h"
#include "smoke/Structs.h"
#include "smoke/TypeCollection.h"
#include "cstdint"
#include "memory"
#include "optional"
#include "string"
#include "vector"

using Structs = ::smoke::Structs;
using Point = ::smoke::Structs::Point;
using Line = ::smoke::Structs::Line;
using AllTypesStruct = ::smoke::Structs::AllTypesStruct;
using NestingImmutableStruct = ::smoke::Structs::NestingImmutableStruct;
using DoubleNestingImmutableStruct = ::smoke::Structs::DoubleNestingImmutableStruct;
using StructWithArrayOfImmutable = ::smoke::Structs::StructWithArrayOfImmutable;
using ImmutableStructWithCppAccessors = ::smoke::Structs::ImmutableStructWithCppAccessors;
using MutableStructWithCppAccessors = ::smoke::Structs::MutableStructWithCppAccessors;
using FooBar = ::smoke::Structs::FooBar;



void register_smoke_Structs(py::module_& module) {
auto cls_Structs = py::class_<Structs, std::shared_ptr<Structs>>(module, "smoke_Structs")
        .def("__gluecodium_id__", [](const Structs& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("swap_point_coordinates", &Structs::swap_point_coordinates, py::arg("input"))
        .def_static("return_all_types_struct", &Structs::return_all_types_struct, py::arg("input"))
        .def_static("create_point", &Structs::create_point, py::arg("x"), py::arg("y"))
        .def_static("modify_all_types_struct", &Structs::modify_all_types_struct, py::arg("input"))
        ;

auto cls_StructsPoint = py::class_<Point>(cls_Structs, "Point")
        .def_readwrite("x", &Point::x)
        .def_readwrite("y", &Point::y)
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def_static("from_polar", &Point::from_polar, py::arg("phi"), py::arg("r"))
        ;

auto cls_StructsLine = py::class_<Line>(cls_Structs, "Line")
        .def_readwrite("a", &Line::a)
        .def_readwrite("b", &Line::b)
        .def(py::init<>())
        .def(py::init<::smoke::Structs::Point, ::smoke::Structs::Point>(), py::arg("a"), py::arg("b"))
        ;

auto cls_StructsAllTypesStruct = py::class_<AllTypesStruct>(cls_Structs, "AllTypesStruct")
        .def_readonly("int8_field", &AllTypesStruct::int8_field)
        .def_readonly("uint8_field", &AllTypesStruct::uint8_field)
        .def_readonly("int16_field", &AllTypesStruct::int16_field)
        .def_readonly("uint16_field", &AllTypesStruct::uint16_field)
        .def_readonly("int32_field", &AllTypesStruct::int32_field)
        .def_readonly("uint32_field", &AllTypesStruct::uint32_field)
        .def_readonly("int64_field", &AllTypesStruct::int64_field)
        .def_readonly("uint64_field", &AllTypesStruct::uint64_field)
        .def_readonly("float_field", &AllTypesStruct::float_field)
        .def_readonly("double_field", &AllTypesStruct::double_field)
        .def_readonly("string_field", &AllTypesStruct::string_field)
        .def_readonly("boolean_field", &AllTypesStruct::boolean_field)
        .def_readonly("bytes_field", &AllTypesStruct::bytes_field)
        .def_readonly("point_field", &AllTypesStruct::point_field)
        .def(py::init<int8_t, uint8_t, int16_t, uint16_t, int32_t, uint32_t, int64_t, uint64_t, float, double, ::std::string, bool, ::std::shared_ptr< ::std::vector< uint8_t > >, ::smoke::Structs::Point>(), py::arg("int8_field"), py::arg("uint8_field"), py::arg("int16_field"), py::arg("uint16_field"), py::arg("int32_field"), py::arg("uint32_field"), py::arg("int64_field"), py::arg("uint64_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("boolean_field"), py::arg("bytes_field"), py::arg("point_field"))
        ;

auto cls_StructsNestingImmutableStruct = py::class_<NestingImmutableStruct>(cls_Structs, "NestingImmutableStruct")
        .def_readonly("struct_field", &NestingImmutableStruct::struct_field)
        .def(py::init<::smoke::Structs::AllTypesStruct>(), py::arg("struct_field"))
        ;

auto cls_StructsDoubleNestingImmutableStruct = py::class_<DoubleNestingImmutableStruct>(cls_Structs, "DoubleNestingImmutableStruct")
        .def_readonly("nesting_struct_field", &DoubleNestingImmutableStruct::nesting_struct_field)
        .def(py::init<::smoke::Structs::NestingImmutableStruct>(), py::arg("nesting_struct_field"))
        ;

auto cls_StructsStructWithArrayOfImmutable = py::class_<StructWithArrayOfImmutable>(cls_Structs, "StructWithArrayOfImmutable")
        .def_readonly("array_field", &StructWithArrayOfImmutable::array_field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::Structs::AllTypesStruct >>(), py::arg("array_field"))
        ;

auto cls_StructsImmutableStructWithCppAccessors = py::class_<ImmutableStructWithCppAccessors>(cls_Structs, "ImmutableStructWithCppAccessors")
        .def_property_readonly("trivial_int_field", static_cast<int32_t (ImmutableStructWithCppAccessors::*)() const>(&ImmutableStructWithCppAccessors::get_trivial_int_field))
        .def_property_readonly("trivial_double_field", static_cast<double (ImmutableStructWithCppAccessors::*)() const>(&ImmutableStructWithCppAccessors::get_trivial_double_field))
        .def_property_readonly("nontrivial_string_field", static_cast<const ::std::string& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_string_field))
        .def_property_readonly("nontrivial_point_field", static_cast<const ::smoke::Structs::Point& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_point_field))
        .def_property_readonly("nontrivial_optional_point", static_cast<const std::optional< ::smoke::Structs::Point >& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_optional_point))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;

auto cls_StructsMutableStructWithCppAccessors = py::class_<MutableStructWithCppAccessors>(cls_Structs, "MutableStructWithCppAccessors")
        .def_property("trivial_int_field", static_cast<int32_t (MutableStructWithCppAccessors::*)() const>(&MutableStructWithCppAccessors::get_trivial_int_field), py::overload_cast<const int32_t>(&MutableStructWithCppAccessors::set_trivial_int_field))
        .def_property("trivial_double_field", static_cast<double (MutableStructWithCppAccessors::*)() const>(&MutableStructWithCppAccessors::get_trivial_double_field), py::overload_cast<const double>(&MutableStructWithCppAccessors::set_trivial_double_field))
        .def_property("nontrivial_string_field", static_cast<const ::std::string& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_string_field), py::overload_cast<const ::std::string&>(&MutableStructWithCppAccessors::set_nontrivial_string_field))
        .def_property("nontrivial_point_field", static_cast<const ::smoke::Structs::Point& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_point_field), py::overload_cast<const ::smoke::Structs::Point&>(&MutableStructWithCppAccessors::set_nontrivial_point_field))
        .def_property("nontrivial_optional_point", static_cast<const std::optional< ::smoke::Structs::Point >& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_optional_point), py::overload_cast<const std::optional< ::smoke::Structs::Point >&>(&MutableStructWithCppAccessors::set_nontrivial_optional_point))
        .def(py::init<>())
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;

auto cls_StructsFooBar = py::enum_<FooBar>(cls_Structs, "FooBar")
        .value("FOO", FooBar::FOO)
        .value("BAR", FooBar::BAR)
        ;


}
