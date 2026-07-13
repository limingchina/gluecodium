

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/RouteUtils.h"
#include "smoke/StructsWithConstantsInterface.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructsWithConstantsInterface = ::gluecodium::smoke::StructsWithConstantsInterface;

void register_StructsWithConstantsInterface(py::module_& module) {
    py::class_<StructsWithConstantsInterface, std::shared_ptr<StructsWithConstantsInterface>>(module, "StructsWithConstantsInterface")
        ;
}

