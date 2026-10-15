

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
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Dates.h"
#include "chrono"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using Dates = ::smoke::Dates;
using DateStruct = ::smoke::Dates::DateStruct;



void register_smoke_Dates(py::module_& module) {
auto cls_Dates = py::class_<Dates, std::shared_ptr<Dates>>(module, "smoke_Dates")
        .def("__gluecodium_id__", [](const Dates& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("date_method", &Dates::date_method, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("nullable_date_method", &Dates::nullable_date_method, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_property("date_property", [](const Dates& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_date_property();
            });
        }, [](Dates& self, const ::std::chrono::system_clock::time_point& value) {
            gluecodium::python::call_native([&] {
                self.set_date_property(value);
            });
        })
        .def_property("date_set", [](const Dates& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_date_set();
            }));
        }, [](Dates& self, const ::std::unordered_set< ::std::chrono::system_clock::time_point, ::gluecodium::hash< ::std::chrono::system_clock::time_point > >& value) {
            gluecodium::python::call_native([&] {
                self.set_date_set(value);
            });
        })
        ;

auto cls_DatesDateStruct = py::class_<DateStruct>(cls_Dates, "DateStruct")
        .def_property("date_field", [](const DateStruct& self) -> decltype(auto) {
            return
                (self.date_field)
            ;
        }, [](DateStruct& self, const ::std::chrono::system_clock::time_point& value) {

                self.date_field = value;

        })
        .def_property("nullable_date_field", [](const DateStruct& self) -> decltype(auto) {
            return
                (self.nullable_date_field)
            ;
        }, [](DateStruct& self, const ::gluecodium::optional< ::std::chrono::system_clock::time_point >& value) {

                self.nullable_date_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point>(), py::arg("date_field"))
        .def(py::init<::std::chrono::system_clock::time_point, ::gluecodium::optional< ::std::chrono::system_clock::time_point >>(), py::arg("date_field"), py::arg("nullable_date_field"))
        ;


}
