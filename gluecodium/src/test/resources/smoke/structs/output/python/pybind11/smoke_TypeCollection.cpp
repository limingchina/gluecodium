

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
#include "smoke/TypeCollection.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

using TypeCollection = ::smoke::TypeCollection;
using Point = ::smoke::TypeCollection::Point;
using Line = ::smoke::TypeCollection::Line;
using AllTypesStruct = ::smoke::TypeCollection::AllTypesStruct;



void register_smoke_TypeCollection(py::module_& module) {
auto cls_TypeCollection = py::class_<TypeCollection>(module, "smoke_TypeCollection")
        .def(py::init<>())
        ;

auto cls_TypeCollectionPoint = py::class_<Point>(cls_TypeCollection, "Point")
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
        ;

auto cls_TypeCollectionLine = py::class_<Line>(cls_TypeCollection, "Line")
        .def_property("a", [](const Line& self) -> decltype(auto) {
            return
                (self.a)
            ;
        }, [](Line& self, const ::smoke::TypeCollection::Point& value) {

                self.a = value;

        })
        .def_property("b", [](const Line& self) -> decltype(auto) {
            return
                (self.b)
            ;
        }, [](Line& self, const ::smoke::TypeCollection::Point& value) {

                self.b = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::TypeCollection::Point, ::smoke::TypeCollection::Point>(), py::arg("a"), py::arg("b"))
        ;

auto cls_TypeCollectionAllTypesStruct = py::class_<AllTypesStruct>(cls_TypeCollection, "AllTypesStruct")
        .def_property("int8_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int8_field)
            ;
        }, [](AllTypesStruct& self, const int8_t value) {

                self.int8_field = value;

        })
        .def_property("uint8_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint8_field)
            ;
        }, [](AllTypesStruct& self, const uint8_t value) {

                self.uint8_field = value;

        })
        .def_property("int16_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int16_field)
            ;
        }, [](AllTypesStruct& self, const int16_t value) {

                self.int16_field = value;

        })
        .def_property("uint16_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint16_field)
            ;
        }, [](AllTypesStruct& self, const uint16_t value) {

                self.uint16_field = value;

        })
        .def_property("int32_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int32_field)
            ;
        }, [](AllTypesStruct& self, const int32_t value) {

                self.int32_field = value;

        })
        .def_property("uint32_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint32_field)
            ;
        }, [](AllTypesStruct& self, const uint32_t value) {

                self.uint32_field = value;

        })
        .def_property("int64_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.int64_field)
            ;
        }, [](AllTypesStruct& self, const int64_t value) {

                self.int64_field = value;

        })
        .def_property("uint64_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.uint64_field)
            ;
        }, [](AllTypesStruct& self, const uint64_t value) {

                self.uint64_field = value;

        })
        .def_property("float_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](AllTypesStruct& self, const float value) {

                self.float_field = value;

        })
        .def_property("double_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](AllTypesStruct& self, const double value) {

                self.double_field = value;

        })
        .def_property("string_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](AllTypesStruct& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("boolean_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.boolean_field)
            ;
        }, [](AllTypesStruct& self, const bool value) {

                self.boolean_field = value;

        })
        .def_property("bytes_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.bytes_field)
            ;
        }, [](AllTypesStruct& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {

                self.bytes_field = value;

        })
        .def_property("point_field", [](const AllTypesStruct& self) -> decltype(auto) {
            return
                (self.point_field)
            ;
        }, [](AllTypesStruct& self, const ::smoke::TypeCollection::Point& value) {

                self.point_field = value;

        })
        .def(py::init<>())
        .def(py::init<int8_t, uint8_t, int16_t, uint16_t, int32_t, uint32_t, int64_t, uint64_t, float, double, ::std::string, bool, ::std::shared_ptr< ::std::vector< uint8_t > >, ::smoke::TypeCollection::Point>(), py::arg("int8_field"), py::arg("uint8_field"), py::arg("int16_field"), py::arg("uint16_field"), py::arg("int32_field"), py::arg("uint32_field"), py::arg("int64_field"), py::arg("uint64_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("boolean_field"), py::arg("bytes_field"), py::arg("point_field"))
        ;


}
