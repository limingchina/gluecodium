

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
#include "gluecodium/VectorHash.h"
#include "smoke/RouteUtils.h"
#include "smoke/StructsWithConstantsInterface.h"
#include "string"
#include "vector"

using StructsWithConstantsInterface = ::smoke::StructsWithConstantsInterface;
using MultiRoute = ::smoke::StructsWithConstantsInterface::MultiRoute;
using StructWithConstantsOnly = ::smoke::StructsWithConstantsInterface::StructWithConstantsOnly;



void register_smoke_StructsWithConstantsInterface(py::module_& module) {
auto cls_StructsWithConstantsInterface = py::class_<StructsWithConstantsInterface, std::shared_ptr<StructsWithConstantsInterface>>(module, "smoke_StructsWithConstantsInterface")
        .def("__gluecodium_id__", [](const StructsWithConstantsInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_StructsWithConstantsInterfaceMultiRoute = py::class_<MultiRoute>(cls_StructsWithConstantsInterface, "MultiRoute")
        .def_readwrite("descriptions", &MultiRoute::descriptions)
        .def_readwrite("type", &MultiRoute::type)
        .def(py::init<>())
        .def(py::init<::std::vector< ::std::string >, ::smoke::RouteUtils::RouteType>(), py::arg("descriptions"), py::arg("type"))
        ;

auto cls_StructsWithConstantsInterfaceStructWithConstantsOnly = py::class_<StructWithConstantsOnly>(cls_StructsWithConstantsInterface, "StructWithConstantsOnly")
        .def(py::init<>())
        ;


}
