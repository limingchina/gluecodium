

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassWithIncludes.h"
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ShouldNotInclude.h"
#include "functional"
#include "memory"

void register_ChildClassWithIncludes(py::module_& module) {
    py::class_<ChildClassWithIncludes>(module, "ChildClassWithIncludes")
        ;
}

