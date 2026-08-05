

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
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DatesSteady.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

using DatesSteady = ::smoke::DatesSteady;
using DateStruct = ::smoke::DatesSteady::DateStruct;



void register_smoke_DatesSteady(py::module_& module) {
auto cls_DatesSteady = py::class_<DatesSteady, std::shared_ptr<DatesSteady>>(module, "smoke_DatesSteady")
        .def("__gluecodium_id__", [](const DatesSteady& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("date_method", &DatesSteady::date_method, py::arg("input"))
        .def("nullable_date_method", &DatesSteady::nullable_date_method, py::arg("input"))
                .def("date_list_method", [](DatesSteady& self, const ::std::vector< std::chrono::steady_clock::time_point >& input) -> py::object {
                        return gluecodium::python::to_python_regular(self.date_list_method(input));
                }, py::arg("input"))
        ;

auto cls_DatesSteadyDateStruct = py::class_<DateStruct>(cls_DatesSteady, "DateStruct")
        .def_readwrite("date_field", &DateStruct::date_field)
        .def_readwrite("nullable_date_field", &DateStruct::nullable_date_field)
        .def(py::init<>())
        .def(py::init<std::chrono::steady_clock::time_point>(), py::arg("date_field"))
        .def(py::init<std::chrono::steady_clock::time_point, std::optional< std::chrono::steady_clock::time_point >>(), py::arg("date_field"), py::arg("nullable_date_field"))
        ;


}
