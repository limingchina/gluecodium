

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Structs.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithArrayOfImmutable = ::smoke::Structs::StructWithArrayOfImmutable;

void register_StructsStructWithArrayOfImmutable(py::module_& module) {
    py::class_<StructWithArrayOfImmutable>(module, "StructsStructWithArrayOfImmutable")
        .def_readonly("array_field", &StructWithArrayOfImmutable::array_field)
        .def(py::init<::std::vector< ::smoke::Structs::AllTypesStruct >>(), py::arg("array_field"))
        ;
}

