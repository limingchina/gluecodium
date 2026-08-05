

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
#include "foo/Bar.h"
#include "smoke/Enums.h"

using Enums = ::smoke::Enums;
using External_Enum = ::smoke::Enums::External_Enum;



void register_smoke_Enums(py::module_& module) {
auto cls_Enums = py::class_<Enums, std::shared_ptr<Enums>>(module, "smoke_Enums")
        .def("__gluecodium_id__", [](const Enums& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("method_with_external_enum", &Enums::method_with_external_enum, py::arg("input"))
        ;

auto cls_EnumsExternal_Enum = py::enum_<External_Enum>(cls_Enums, "ExternalEnum")
        .value("FOO_VALUE", External_Enum::Foo_Value)
        .value("BAR_VALUE", External_Enum::Bar_Value)
        ;

auto cls_EnumsVeryExternalEnum = py::enum_<::fire::SomeVeryExternalEnum>(cls_Enums, "VeryExternalEnum")
        .value("FOO", ::fire::SomeVeryExternalEnum::FOO)
        .value("BAR", ::fire::SomeVeryExternalEnum::BAR)
        ;


}
