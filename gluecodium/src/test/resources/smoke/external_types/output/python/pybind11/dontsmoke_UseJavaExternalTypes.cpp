

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "dontsmoke/UseJavaExternalTypes.h"
#include "smoke/Currency.h"
#include "smoke/JavaExternalTypesStruct.h"
#include "smoke/Month.h"
#include "smoke/Season.h"
#include "smoke/SystemColor.h"
#include "smoke/TimeZone.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseJavaExternalTypes = ::dontsmoke::UseJavaExternalTypes;


void register_dontsmoke_UseJavaExternalTypes(py::module_& module) {
    py::class_<UseJavaExternalTypes, std::shared_ptr<UseJavaExternalTypes>>(module, "UseJavaExternalTypes")
        ;
}

