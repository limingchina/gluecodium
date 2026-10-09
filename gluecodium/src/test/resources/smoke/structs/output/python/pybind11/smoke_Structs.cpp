

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
#include "gluecodium/Optional.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Structs.h"
#include "smoke/TypeCollection.h"
#include "cstdint"
#include "memory"
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
            return gluecodium::python::native_identity(self);
        })
        .def_static("swap_point_coordinates", &Structs::swap_point_coordinates, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("return_all_types_struct", &Structs::return_all_types_struct, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("create_point", &Structs::create_point, py::arg("x"), py::arg("y"), py::call_guard<py::gil_scoped_release>())
        .def_static("modify_all_types_struct", &Structs::modify_all_types_struct, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        ;

auto cls_StructsPoint = py::class_<Point>(cls_Structs, "Point")
        .def_property("x", [](const Point& self) -> decltype(auto) {
            return
                (self.x)
            ;
        }, [](Point& self, const double value) {

                self.x = value;

        })
        .def_property("y", [](const Point& self) -> decltype(auto) {
            return
                (self.y)
            ;
        }, [](Point& self, const double value) {

                self.y = value;

        })
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def_static("from_polar", &Point::from_polar, py::arg("phi"), py::arg("r"), py::call_guard<py::gil_scoped_release>())
        ;

auto cls_StructsLine = py::class_<Line>(cls_Structs, "Line")
        .def_property("a", [](const Line& self) -> decltype(auto) {
            return
                (self.a)
            ;
        }, [](Line& self, const ::smoke::Structs::Point& value) {

                self.a = value;

        })
        .def_property("b", [](const Line& self) -> decltype(auto) {
            return
                (self.b)
            ;
        }, [](Line& self, const ::smoke::Structs::Point& value) {

                self.b = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::Structs::Point, ::smoke::Structs::Point>(), py::arg("a"), py::arg("b"))
        ;

auto cls_StructsAllTypesStruct = py::class_<AllTypesStruct>(cls_Structs, "AllTypesStruct")
        .def_property_readonly("int8_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int8_field)
            ;
        })
        .def_property_readonly("uint8_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint8_field)
            ;
        })
        .def_property_readonly("int16_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int16_field)
            ;
        })
        .def_property_readonly("uint16_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint16_field)
            ;
        })
        .def_property_readonly("int32_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int32_field)
            ;
        })
        .def_property_readonly("uint32_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint32_field)
            ;
        })
        .def_property_readonly("int64_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int64_field)
            ;
        })
        .def_property_readonly("uint64_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint64_field)
            ;
        })
        .def_property_readonly("float_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        })
        .def_property_readonly("double_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        })
        .def_property_readonly("string_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        })
        .def_property_readonly("boolean_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.boolean_field)
            ;
        })
        .def_property_readonly("bytes_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.bytes_field)
            ;
        })
        .def_property_readonly("point_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.point_field)
            ;
        })
        .def(py::init<int8_t, uint8_t, int16_t, uint16_t, int32_t, uint32_t, int64_t, uint64_t, float, double, ::std::string, bool, ::std::shared_ptr< ::std::vector< uint8_t > >, ::smoke::Structs::Point>(), py::arg("int8_field"), py::arg("uint8_field"), py::arg("int16_field"), py::arg("uint16_field"), py::arg("int32_field"), py::arg("uint32_field"), py::arg("int64_field"), py::arg("uint64_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("boolean_field"), py::arg("bytes_field"), py::arg("point_field"))
        ;

auto cls_StructsNestingImmutableStruct = py::class_<NestingImmutableStruct>(cls_Structs, "NestingImmutableStruct")
        .def_property_readonly("struct_field", [](const NestingImmutableStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        })
        .def(py::init<::smoke::Structs::AllTypesStruct>(), py::arg("struct_field"))
        ;

auto cls_StructsDoubleNestingImmutableStruct = py::class_<DoubleNestingImmutableStruct>(cls_Structs, "DoubleNestingImmutableStruct")
        .def_property_readonly("nesting_struct_field", [](const DoubleNestingImmutableStruct& self) -> decltype(auto) {
            return
                (self.nesting_struct_field)
            ;
        })
        .def(py::init<::smoke::Structs::NestingImmutableStruct>(), py::arg("nesting_struct_field"))
        ;

auto cls_StructsStructWithArrayOfImmutable = py::class_<StructWithArrayOfImmutable>(cls_Structs, "StructWithArrayOfImmutable")
        .def_property_readonly("array_field", [](const StructWithArrayOfImmutable& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.array_field)
            );
        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::Structs::AllTypesStruct >>(), py::arg("array_field"))
        ;

auto cls_StructsImmutableStructWithCppAccessors = py::class_<ImmutableStructWithCppAccessors>(cls_Structs, "ImmutableStructWithCppAccessors")
        .def_property_readonly("trivial_int_field", [](const ImmutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_trivial_int_field();
            });
        })
        .def_property_readonly("trivial_double_field", [](const ImmutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_trivial_double_field();
            });
        })
        .def_property_readonly("nontrivial_string_field", [](const ImmutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_string_field();
            });
        })
        .def_property_readonly("nontrivial_point_field", [](const ImmutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_point_field();
            });
        })
        .def_property_readonly("nontrivial_optional_point", [](const ImmutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_optional_point();
            });
        })
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, ::gluecodium::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;

auto cls_StructsMutableStructWithCppAccessors = py::class_<MutableStructWithCppAccessors>(cls_Structs, "MutableStructWithCppAccessors")
        .def_property("trivial_int_field", [](const MutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_trivial_int_field();
            });
        }, [](MutableStructWithCppAccessors& self, const int32_t value) {
            gluecodium::python::call_native([&] {
                self.set_trivial_int_field(value);
            });
        })
        .def_property("trivial_double_field", [](const MutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_trivial_double_field();
            });
        }, [](MutableStructWithCppAccessors& self, const double value) {
            gluecodium::python::call_native([&] {
                self.set_trivial_double_field(value);
            });
        })
        .def_property("nontrivial_string_field", [](const MutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_string_field();
            });
        }, [](MutableStructWithCppAccessors& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_nontrivial_string_field(value);
            });
        })
        .def_property("nontrivial_point_field", [](const MutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_point_field();
            });
        }, [](MutableStructWithCppAccessors& self, const ::smoke::Structs::Point& value) {
            gluecodium::python::call_native([&] {
                self.set_nontrivial_point_field(value);
            });
        })
        .def_property("nontrivial_optional_point", [](const MutableStructWithCppAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_nontrivial_optional_point();
            });
        }, [](MutableStructWithCppAccessors& self, const ::gluecodium::optional< ::smoke::Structs::Point >& value) {
            gluecodium::python::call_native([&] {
                self.set_nontrivial_optional_point(value);
            });
        })
        .def(py::init<>())
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, ::gluecodium::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;

auto cls_StructsFooBar = py::enum_<FooBar>(cls_Structs, "FooBar")
        .value("FOO", FooBar::FOO)
        .value("BAR", FooBar::BAR)
        ;


}
