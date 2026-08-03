

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
#include "smoke/CtorLinks.h"
#include "cstdint"
#include "memory"
#include "string"

using CtorLinks = ::smoke::CtorLinks;
using SingleCtor = ::smoke::CtorLinks::SingleCtor;
using SingleCtorWithOneArgument = ::smoke::CtorLinks::SingleCtorWithOneArgument;
using SingleCtorWithTwoArgument = ::smoke::CtorLinks::SingleCtorWithTwoArgument;
using OverloadedCtors = ::smoke::CtorLinks::OverloadedCtors;



void register_smoke_CtorLinks(py::module_& module) {
auto cls_CtorLinks = py::class_<CtorLinks, std::shared_ptr<CtorLinks>>(module, "smoke_CtorLinks")
        .def("__gluecodium_id__", [](const CtorLinks& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_CtorLinksSingleCtor = py::class_<SingleCtor, std::shared_ptr<SingleCtor>>(cls_CtorLinks, "SingleCtor")
        .def("__gluecodium_id__", [](const SingleCtor& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &SingleCtor::create)
        ;

auto cls_CtorLinksSingleCtorWithOneArgument = py::class_<SingleCtorWithOneArgument, std::shared_ptr<SingleCtorWithOneArgument>>(cls_CtorLinks, "SingleCtorWithOneArgument")
        .def("__gluecodium_id__", [](const SingleCtorWithOneArgument& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &SingleCtorWithOneArgument::create, py::arg("arg"))
        ;

auto cls_CtorLinksSingleCtorWithTwoArgument = py::class_<SingleCtorWithTwoArgument, std::shared_ptr<SingleCtorWithTwoArgument>>(cls_CtorLinks, "SingleCtorWithTwoArgument")
        .def("__gluecodium_id__", [](const SingleCtorWithTwoArgument& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &SingleCtorWithTwoArgument::create, py::arg("arg"), py::arg("arg2"))
        ;

auto cls_CtorLinksOverloadedCtors = py::class_<OverloadedCtors, std::shared_ptr<OverloadedCtors>>(cls_CtorLinks, "OverloadedCtors")
        .def("__gluecodium_id__", [](const OverloadedCtors& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", py::overload_cast<const ::std::string&>(OverloadedCtors::create), py::arg("input"))
        .def_static("create", py::overload_cast<const ::std::string&, const bool>(OverloadedCtors::create), py::arg("input"), py::arg("flag"))
        ;


}
