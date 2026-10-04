

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

using TypeCollection = ::smoke::TypeCollection;
using Point = ::smoke::TypeCollection::Point;
using StructHavingAliasFieldDefinedBelow = ::smoke::TypeCollection::StructHavingAliasFieldDefinedBelow;



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

auto cls_TypeCollectionStructHavingAliasFieldDefinedBelow = py::class_<StructHavingAliasFieldDefinedBelow>(cls_TypeCollection, "StructHavingAliasFieldDefinedBelow")
        .def_property("field", [](const StructHavingAliasFieldDefinedBelow& self) -> decltype(auto) {
            return
                (self.field)
            ;
        }, [](StructHavingAliasFieldDefinedBelow& self, const uint64_t value) {

                self.field = value;

        })
        .def(py::init<>())
        .def(py::init<uint64_t>(), py::arg("field"))
        ;


}
