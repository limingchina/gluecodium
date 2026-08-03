

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
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/Enums.h"
#include "cstdint"
#include "string"
#include "unordered_map"

using Enums = ::smoke::Enums;
using ErrorStruct = ::smoke::Enums::ErrorStruct;
using SimpleEnum = ::smoke::Enums::SimpleEnum;
using InternalErrorCode = ::smoke::Enums::InternalErrorCode;



void register_smoke_Enums(py::module_& module) {
auto cls_Enums = py::class_<Enums, std::shared_ptr<Enums>>(module, "smoke_Enums")
        .def("__gluecodium_id__", [](const Enums& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("method_with_enumeration", &Enums::method_with_enumeration, py::arg("input"))
        .def_static("flip_enum_value", &Enums::flip_enum_value, py::arg("input"))
        .def_static("extract_enum_from_struct", &Enums::extract_enum_from_struct, py::arg("input"))
        .def_static("create_struct_with_enum_inside", &Enums::create_struct_with_enum_inside, py::arg("type"), py::arg("message"))
        ;

auto cls_EnumsErrorStruct = py::class_<ErrorStruct>(cls_Enums, "ErrorStruct")
        .def_readwrite("type", &ErrorStruct::type)
        .def_readwrite("message", &ErrorStruct::message)
        .def(py::init<>())
        .def(py::init<::smoke::Enums::InternalErrorCode, ::std::string>(), py::arg("type"), py::arg("message"))
        ;

auto cls_EnumsSimpleEnum = py::enum_<SimpleEnum>(cls_Enums, "SimpleEnum")
        .value("FIRST", SimpleEnum::FIRST)
        .value("SECOND", SimpleEnum::SECOND)
        ;

auto cls_EnumsInternalErrorCode = py::enum_<InternalErrorCode>(cls_Enums, "InternalErrorCode")
        .value("ERROR_NONE", InternalErrorCode::ERROR_NONE)
        .value("ERROR_FATAL", InternalErrorCode::ERROR_FATAL)
        ;


}
