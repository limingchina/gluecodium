

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/StructsQualifiedType.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Structs.h"
#include "smoke/StructsInstance.h"
#include "smoke/TypeCollection.h"
#include "memory"
#include "vector"

void register_StructsQualifiedType(py::module_& module) {
    py::class_<StructsQualifiedType>(module, "StructsQualifiedType")
        ;
}

