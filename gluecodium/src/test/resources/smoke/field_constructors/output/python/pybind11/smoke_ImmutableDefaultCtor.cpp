

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
#include "smoke/ImmutableDefaultCtor.h"
#include "string"

using ImmutableDefaultCtor = ::smoke::ImmutableDefaultCtor;



void register_smoke_ImmutableDefaultCtor(py::module_& module) {
auto cls_ImmutableDefaultCtor = py::class_<ImmutableDefaultCtor>(module, "smoke_ImmutableDefaultCtor")
        .def_property("string_field", [](const ImmutableDefaultCtor& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](ImmutableDefaultCtor& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        ;


}
