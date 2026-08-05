

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/ImmutableStructWithDefaults.h"
#include "smoke/PosDefaultStructWithCustomStructsFields.h"
#include "smoke/PosDefaultStructWithFieldUsingImmutableStruct.h"
#include "smoke/SomeMutableCustomStructWithDefaults.h"
#include "smoke/StructWithAllDefaults.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "cstdint"
#include "memory"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

using PosDefaultStructWithCustomStructsFields = ::smoke::PosDefaultStructWithCustomStructsFields;



void register_smoke_PosDefaultStructWithCustomStructsFields(py::module_& module) {
auto cls_PosDefaultStructWithCustomStructsFields = py::class_<PosDefaultStructWithCustomStructsFields>(module, "smoke_PosDefaultStructWithCustomStructsFields")
        .def_readonly("const_ctor_field0", &PosDefaultStructWithCustomStructsFields::const_ctor_field0)
        .def_readonly("const_ctor_field1", &PosDefaultStructWithCustomStructsFields::const_ctor_field1)
        .def_readwrite("const_ctor_field2", &PosDefaultStructWithCustomStructsFields::const_ctor_field2)
        .def_readwrite("const_ctor_field3", &PosDefaultStructWithCustomStructsFields::const_ctor_field3)
        .def_readwrite("const_ctor_field4", &PosDefaultStructWithCustomStructsFields::const_ctor_field4)
        .def_readwrite("const_ctor_field5", &PosDefaultStructWithCustomStructsFields::const_ctor_field5)
        .def_readonly("const_ctor_field6", &PosDefaultStructWithCustomStructsFields::const_ctor_field6)
        .def_readonly("const_ctor_field7", &PosDefaultStructWithCustomStructsFields::const_ctor_field7)
        .def_readwrite("non_const_ctor_field0", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field0)
        .def_readonly("non_const_ctor_field1", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field1)
        .def_readwrite("non_const_ctor_field2", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field2)
        .def_readwrite("non_const_ctor_field3", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field3)
        .def_readwrite("non_const_ctor_field4", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field4)
        .def_readwrite("non_const_ctor_field5", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field5)
        .def_readwrite("non_const_ctor_field6", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field6)
        .def_readwrite("non_const_ctor_field7", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field7)
        .def(py::init<>())
        .def(py::init<::smoke::ImmutableStructWithDefaults, std::optional< ::smoke::ImmutableStructWithDefaults >, ::std::vector< ::std::string >, std::optional< ::std::unordered_map< ::std::string, ::std::string > >, int32_t, double, std::optional< ::smoke::ImmutableStructWithDefaults >, std::optional< ::smoke::ImmutableStructWithDefaults >, ::smoke::StructWithAllDefaults, ::smoke::PosDefaultStructWithFieldUsingImmutableStruct, ::smoke::SomeMutableCustomStructWithDefaults, ::smoke::StructWithNullableCollectionDefaults, std::optional< ::smoke::StructWithAllDefaults >, ::std::shared_ptr< ::std::vector< uint8_t > >, ::std::shared_ptr< ::std::vector< uint8_t > >, std::optional< ::std::shared_ptr< ::std::vector< uint8_t > > >>(), py::arg("const_ctor_field0"), py::arg("const_ctor_field1"), py::arg("const_ctor_field2"), py::arg("const_ctor_field3"), py::arg("const_ctor_field4"), py::arg("const_ctor_field5"), py::arg("const_ctor_field6"), py::arg("const_ctor_field7"), py::arg("non_const_ctor_field0"), py::arg("non_const_ctor_field1"), py::arg("non_const_ctor_field2"), py::arg("non_const_ctor_field3"), py::arg("non_const_ctor_field4"), py::arg("non_const_ctor_field5"), py::arg("non_const_ctor_field6"), py::arg("non_const_ctor_field7"))
        ;


}
