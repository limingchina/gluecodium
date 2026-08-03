

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
#include "smoke/NestedReferences.h"
#include "memory"
#include "string"

using NestedReferences = ::smoke::NestedReferences;
using NestedReferences = ::smoke::NestedReferences::NestedReferences;



void register_smoke_NestedReferences(py::module_& module) {
auto cls_NestedReferences = py::class_<NestedReferences, std::shared_ptr<NestedReferences>>(module, "smoke_NestedReferences")
        .def("__gluecodium_id__", [](const NestedReferences& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("inside_out", &NestedReferences::inside_out, py::arg("struct1"), py::arg("struct2"))
        ;

auto cls_NestedReferencesNestedReferences = py::class_<NestedReferences>(cls_NestedReferences, "NestedReferences")
        .def_readwrite("string_field", &NestedReferences::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
