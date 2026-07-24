

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/TypeCollection.h"
#include "smoke/TypeDefs.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using TypeDefs = ::smoke::TypeDefs;


void register_smoke_TypeDefs(py::module_& module) {
    py::class_<TypeDefs, std::shared_ptr<TypeDefs>>(module, "TypeDefs")
        .def_property("primitive_type_property", py::overload_cast<>(&TypeDefs::get_primitive_type_property, py::const_), py::overload_cast<const ::std::vector< double >&>(&TypeDefs::set_primitive_type_property))
        ;
}

