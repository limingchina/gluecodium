

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
#include "smoke/Alphabet.h"
#include "smoke/LearnToRead.h"
#include "smoke/foo/Alphabet.h"

using LearnToRead = ::smoke::LearnToRead;



void register_smoke_LearnToRead(py::module_& module) {
auto cls_LearnToRead = py::class_<LearnToRead>(module, "smoke_LearnToRead")
        .def_property("field_a", [](const LearnToRead& self) -> decltype(auto) {
            return
                (self.field_a)
            ;
        }, [](LearnToRead& self, const ::smoke::Alphabet value) {

                self.field_a = value;

        })
        .def_property("field_b", [](const LearnToRead& self) -> decltype(auto) {
            return
                (self.field_b)
            ;
        }, [](LearnToRead& self, const ::smoke::foo::Alphabet value) {

                self.field_b = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::Alphabet, ::smoke::foo::Alphabet>(), py::arg("field_a"), py::arg("field_b"))
        ;


}
