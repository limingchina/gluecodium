

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
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

void register_PosDefaultStructWithCustomStructsFields(py::module_& module) {
    py::class_<PosDefaultStructWithCustomStructsFields>(module, "PosDefaultStructWithCustomStructsFields")
        .def_readwrite("const_ctor_field0", &PosDefaultStructWithCustomStructsFields::const_ctor_field0)
        .def_readwrite("const_ctor_field1", &PosDefaultStructWithCustomStructsFields::const_ctor_field1)
        .def_readwrite("const_ctor_field2", &PosDefaultStructWithCustomStructsFields::const_ctor_field2)
        .def_readwrite("const_ctor_field3", &PosDefaultStructWithCustomStructsFields::const_ctor_field3)
        .def_readwrite("const_ctor_field4", &PosDefaultStructWithCustomStructsFields::const_ctor_field4)
        .def_readwrite("const_ctor_field5", &PosDefaultStructWithCustomStructsFields::const_ctor_field5)
        .def_readwrite("const_ctor_field6", &PosDefaultStructWithCustomStructsFields::const_ctor_field6)
        .def_readwrite("const_ctor_field7", &PosDefaultStructWithCustomStructsFields::const_ctor_field7)
        .def_readwrite("non_const_ctor_field0", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field0)
        .def_readwrite("non_const_ctor_field1", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field1)
        .def_readwrite("non_const_ctor_field2", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field2)
        .def_readwrite("non_const_ctor_field3", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field3)
        .def_readwrite("non_const_ctor_field4", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field4)
        .def_readwrite("non_const_ctor_field5", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field5)
        .def_readwrite("non_const_ctor_field6", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field6)
        .def_readwrite("non_const_ctor_field7", &PosDefaultStructWithCustomStructsFields::non_const_ctor_field7)
        ;
}

