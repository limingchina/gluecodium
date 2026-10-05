

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
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/StructWithSet.h"
#include "unordered_set"

using StructWithSet = ::smoke::StructWithSet;



void register_smoke_StructWithSet(py::module_& module) {
auto cls_StructWithSet = py::class_<StructWithSet>(module, "smoke_StructWithSet")
        .def_property("field", [](const StructWithSet& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.field)
            );
        }, [](StructWithSet& self, const ::std::unordered_set< ::smoke::StructWithSet, ::gluecodium::hash< ::smoke::StructWithSet > >& value) {

                self.field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::unordered_set< ::smoke::StructWithSet, ::gluecodium::hash< ::smoke::StructWithSet > >>(), py::arg("field"))
        .def("__gluecodium_copy__", [](const StructWithSet& self) { return StructWithSet(self); })
        .def("__gluecodium_equals__", [](const StructWithSet& lhs, const StructWithSet& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const StructWithSet& self) { return gluecodium::hash<StructWithSet>{}(self); })
        ;


}
