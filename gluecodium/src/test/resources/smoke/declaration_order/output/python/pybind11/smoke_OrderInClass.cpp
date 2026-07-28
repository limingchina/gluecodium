

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OrderInClass.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OrderInClass = ::smoke::OrderInClass;


void register_smoke_OrderInClass(py::module_& module) {
    py::class_<OrderInClass, std::shared_ptr<OrderInClass>>(module, "smoke_OrderInClass")
        .def("__gluecodium_id__", [](const OrderInClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

