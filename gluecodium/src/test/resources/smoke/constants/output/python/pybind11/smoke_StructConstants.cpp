

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
#include "smoke/StructConstants.h"
#include "string"

using StructConstants = ::smoke::StructConstants;
using SomeStruct = ::smoke::StructConstants::SomeStruct;
using NestingStruct = ::smoke::StructConstants::NestingStruct;



void register_smoke_StructConstants(py::module_& module) {
auto cls_StructConstants = py::class_<StructConstants, std::shared_ptr<StructConstants>>(module, "smoke_StructConstants")
        .def("__gluecodium_id__", [](const StructConstants& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_StructConstantsSomeStruct = py::class_<SomeStruct>(cls_StructConstants, "SomeStruct")
        .def_readwrite("string_field", &SomeStruct::string_field)
        .def_readwrite("float_field", &SomeStruct::float_field)
        .def(py::init<>())
        .def(py::init<::std::string, float>(), py::arg("string_field"), py::arg("float_field"))
        ;

auto cls_StructConstantsNestingStruct = py::class_<NestingStruct>(cls_StructConstants, "NestingStruct")
        .def_readwrite("struct_field", &NestingStruct::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::StructConstants::SomeStruct>(), py::arg("struct_field"))
        ;


}
