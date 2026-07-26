

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
#include "smoke/Structs.h"
#include "cstdint"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithCppAccessors = ::smoke::Structs::ImmutableStructWithCppAccessors;

void register_smoke_StructsImmutableStructWithCppAccessors(py::module_& module) {
    py::class_<ImmutableStructWithCppAccessors>(module, "smoke_StructsImmutableStructWithCppAccessors")
        .def_property_readonly("trivial_int_field", static_cast<int32_t (ImmutableStructWithCppAccessors::*)() const>(&ImmutableStructWithCppAccessors::get_trivial_int_field))
        .def_property_readonly("trivial_double_field", static_cast<double (ImmutableStructWithCppAccessors::*)() const>(&ImmutableStructWithCppAccessors::get_trivial_double_field))
        .def_property_readonly("nontrivial_string_field", static_cast<const ::std::string& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_string_field))
        .def_property_readonly("nontrivial_point_field", static_cast<const ::smoke::Structs::Point& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_point_field))
        .def_property_readonly("nontrivial_optional_point", static_cast<const std::optional< ::smoke::Structs::Point >& (ImmutableStructWithCppAccessors::*)() const &>(&ImmutableStructWithCppAccessors::get_nontrivial_optional_point))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;
}

