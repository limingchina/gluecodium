

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DateInterval.h"
#include "smoke/Persistence.h"
#include "smoke/PseudoColor.h"
#include "smoke/SwiftSeason.h"
#include "smoke/UseSwiftExternalTypes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseSwiftExternalTypes = ::smoke::UseSwiftExternalTypes;


void register_smoke_UseSwiftExternalTypes(py::module_& module) {
    py::class_<UseSwiftExternalTypes, std::shared_ptr<UseSwiftExternalTypes>>(module, "UseSwiftExternalTypes")
        ;
}

