

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
#include "gluecodium/VectorHash.h"
#include "smoke/Alphabet.h"
#include "smoke/NameClashLists.h"
#include "smoke/foo/Alphabet.h"
#include "vector"

using NameClashLists = ::smoke::NameClashLists;



void register_smoke_NameClashLists(py::module_& module) {
auto cls_NameClashLists = py::class_<NameClashLists>(module, "smoke_NameClashLists")
        .def_property("field_a", [](const NameClashLists& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.field_a)
            );
        }, [](NameClashLists& self, const ::std::vector< ::smoke::Alphabet >& value) {

                self.field_a = value;

        })
        .def_property("field_b", [](const NameClashLists& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.field_b)
            );
        }, [](NameClashLists& self, const ::std::vector< ::smoke::foo::Alphabet >& value) {

                self.field_b = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::Alphabet >, ::std::vector< ::smoke::foo::Alphabet >>(), py::arg("field_a"), py::arg("field_b"))
        ;


}
