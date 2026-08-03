

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
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Dates.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using Dates = ::smoke::Dates;
using DateStruct = ::smoke::Dates::DateStruct;



void register_smoke_Dates(py::module_& module) {
auto cls_Dates = py::class_<Dates, std::shared_ptr<Dates>>(module, "smoke_Dates")
        .def("__gluecodium_id__", [](const Dates& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("date_method", &Dates::date_method, py::arg("input"))
        .def("nullable_date_method", &Dates::nullable_date_method, py::arg("input"))
        .def_property("date_property", py::overload_cast<>(&Dates::get_date_property, py::const_), py::overload_cast<const ::std::chrono::system_clock::time_point&>(&Dates::set_date_property))
        .def_property("date_set", py::overload_cast<>(&Dates::get_date_set, py::const_), py::overload_cast<const ::std::unordered_set< ::std::chrono::system_clock::time_point, ::gluecodium::hash< ::std::chrono::system_clock::time_point > >&>(&Dates::set_date_set))
        ;

auto cls_DatesDateStruct = py::class_<DateStruct>(cls_Dates, "DateStruct")
        .def_readwrite("date_field", &DateStruct::date_field)
        .def_readwrite("nullable_date_field", &DateStruct::nullable_date_field)
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point>(), py::arg("date_field"))
        .def(py::init<::std::chrono::system_clock::time_point, std::optional< ::std::chrono::system_clock::time_point >>(), py::arg("date_field"), py::arg("nullable_date_field"))
        ;


}
