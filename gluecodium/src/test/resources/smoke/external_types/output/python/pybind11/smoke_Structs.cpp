

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
#include "foo/Bazz.h"
#include "gluecodium/VectorHash.h"
#include "non/Sense.h"
#include "smoke/Structs.h"
#include "cstdint"
#include "string"
#include "vector"

using Structs = ::smoke::Structs;
using ExternalStruct = ::smoke::Structs::ExternalStruct;



void register_smoke_Structs(py::module_& module) {
auto cls_Structs = py::class_<Structs, std::shared_ptr<Structs>>(module, "smoke_Structs")
        .def("__gluecodium_id__", [](const Structs& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("get_external_struct", &Structs::get_external_struct)
        .def_static("get_another_external_struct", &Structs::get_another_external_struct)
        ;

auto cls_StructsExternalStruct = py::class_<ExternalStruct>(cls_Structs, "ExternalStruct")
        ;

auto cls_StructsAnotherExternalStruct = py::class_<::fire::SomeVeryExternalStruct>(cls_Structs, "AnotherExternalStruct")
        ;


}
