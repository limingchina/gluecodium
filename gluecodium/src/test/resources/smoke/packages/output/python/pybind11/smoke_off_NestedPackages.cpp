

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
#include "smoke/off/NestedPackages.h"
#include "string"

using NestedPackages = ::smoke::off::NestedPackages;
using SomeStruct = ::smoke::off::NestedPackages::SomeStruct;



void register_smoke_off_NestedPackages(py::module_& module) {
auto cls_NestedPackages = py::class_<NestedPackages, std::shared_ptr<NestedPackages>>(module, "smoke_off_NestedPackages")
        .def("__gluecodium_id__", [](const NestedPackages& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("basic_method", &NestedPackages::basic_method, py::arg("input"))
        ;

auto cls_NestedPackagesSomeStruct = py::class_<SomeStruct>(cls_NestedPackages, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;


}
