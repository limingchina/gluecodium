

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
using MutableStructWithCppAccessors = ::smoke::Structs::MutableStructWithCppAccessors;

void register_smoke_StructsMutableStructWithCppAccessors(py::module_& module) {
    py::class_<MutableStructWithCppAccessors>(module, "smoke_StructsMutableStructWithCppAccessors")
        .def_property("trivial_int_field", static_cast<int32_t (MutableStructWithCppAccessors::*)() const>(&MutableStructWithCppAccessors::get_trivial_int_field), py::overload_cast<const int32_t>(&MutableStructWithCppAccessors::set_trivial_int_field))
        .def_property("trivial_double_field", static_cast<double (MutableStructWithCppAccessors::*)() const>(&MutableStructWithCppAccessors::get_trivial_double_field), py::overload_cast<const double>(&MutableStructWithCppAccessors::set_trivial_double_field))
        .def_property("nontrivial_string_field", static_cast<const ::std::string& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_string_field), py::overload_cast<const ::std::string&>(&MutableStructWithCppAccessors::set_nontrivial_string_field))
        .def_property("nontrivial_point_field", static_cast<const ::smoke::Structs::Point& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_point_field), py::overload_cast<const ::smoke::Structs::Point&>(&MutableStructWithCppAccessors::set_nontrivial_point_field))
        .def_property("nontrivial_optional_point", static_cast<const std::optional< ::smoke::Structs::Point >& (MutableStructWithCppAccessors::*)() const &>(&MutableStructWithCppAccessors::get_nontrivial_optional_point), py::overload_cast<const std::optional< ::smoke::Structs::Point >&>(&MutableStructWithCppAccessors::set_nontrivial_optional_point))
        .def(py::init<>())
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"))
        .def(py::init<int32_t, double, ::std::string, ::smoke::Structs::Point, std::optional< ::smoke::Structs::Point >>(), py::arg("trivial_int_field"), py::arg("trivial_double_field"), py::arg("nontrivial_string_field"), py::arg("nontrivial_point_field"), py::arg("nontrivial_optional_point"))
        ;
}

