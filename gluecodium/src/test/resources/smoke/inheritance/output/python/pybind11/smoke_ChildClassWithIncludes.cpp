

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassWithIncludes.h"
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ShouldNotInclude.h"
#include "functional"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildClassWithIncludes = ::smoke::ChildClassWithIncludes;

void register_ChildClassWithIncludes(py::module_& module) {
    py::class_<ChildClassWithIncludes, std::shared_ptr<ChildClassWithIncludes>>(module, "ChildClassWithIncludes")
        ;
}

