

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
#include "smoke/ImmutableNamelessCtor.h"
#include "smoke/MutableStructImmutableFieldsNameless.h"
#include "cstdint"

using MutableStructImmutableFieldsNameless = ::smoke::MutableStructImmutableFieldsNameless;



void register_smoke_MutableStructImmutableFieldsNameless(py::module_& module) {
auto cls_MutableStructImmutableFieldsNameless = py::class_<MutableStructImmutableFieldsNameless>(module, "smoke_MutableStructImmutableFieldsNameless")
        .def_property("struct_field", [](const MutableStructImmutableFieldsNameless& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](MutableStructImmutableFieldsNameless& self, const ::smoke::ImmutableNamelessCtor& value) {

                self.struct_field = value;

        })
        .def_property("int_field", [](const MutableStructImmutableFieldsNameless& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](MutableStructImmutableFieldsNameless& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("bool_field", [](const MutableStructImmutableFieldsNameless& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](MutableStructImmutableFieldsNameless& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<>())
        ;


}
