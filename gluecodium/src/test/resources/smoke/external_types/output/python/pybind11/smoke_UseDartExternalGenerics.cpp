

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CompressionState.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalGenerics.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseDartExternalGenerics = ::smoke::UseDartExternalGenerics;


void register_smoke_UseDartExternalGenerics(py::module_& module) {
    py::class_<UseDartExternalGenerics, std::shared_ptr<UseDartExternalGenerics>>(module, "smoke_UseDartExternalGenerics")
        .def("__gluecodium_id__", [](const UseDartExternalGenerics& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
                .def("use_generics", [](UseDartExternalGenerics& self, const ::std::vector< ::smoke::Rectangle >& list, const ::std::unordered_set< ::smoke::CompressionState, ::gluecodium::hash< ::smoke::CompressionState > >& set) -> py::object {
                        return gluecodium::python::to_python_regular(self.use_generics(list, set));
                }, py::arg("list"), py::arg("set"))
        ;
}

