

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
#include "smoke/ImmutableStructWithClash.h"
#include "cstdint"
#include "string"

using ImmutableStructWithClash = ::smoke::ImmutableStructWithClash;



void register_smoke_ImmutableStructWithClash(py::module_& module) {
auto cls_ImmutableStructWithClash = py::class_<ImmutableStructWithClash>(module, "smoke_ImmutableStructWithClash")
        .def_property_readonly("string_field", [](const ImmutableStructWithClash& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        })
        .def_property_readonly("int_field", [](const ImmutableStructWithClash& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        })
        .def_property_readonly("bool_field", [](const ImmutableStructWithClash& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        })
        .def(py::init<>())
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;


}
