

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
#include "smoke/ImmutableStructNoClash.h"
#include "smoke/MutableStructImmutableFields.h"
#include "cstdint"

using MutableStructImmutableFields = ::smoke::MutableStructImmutableFields;



void register_smoke_MutableStructImmutableFields(py::module_& module) {
auto cls_MutableStructImmutableFields = py::class_<MutableStructImmutableFields>(module, "smoke_MutableStructImmutableFields")
        .def_property_readonly("struct_field", [](const MutableStructImmutableFields& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        })
        .def_property("int_field", [](const MutableStructImmutableFields& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](MutableStructImmutableFields& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("bool_field", [](const MutableStructImmutableFields& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](MutableStructImmutableFields& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<::smoke::ImmutableStructNoClash, int32_t, bool>(), py::arg("struct_field"), py::arg("int_field"), py::arg("bool_field"))
        .def(py::init<>())
        ;


}
