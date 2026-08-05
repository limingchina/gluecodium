

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Lambdas.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

using Lambdas = ::smoke::Lambdas;



void register_smoke_Lambdas(py::module_& module) {
auto cls_Lambdas = py::class_<Lambdas, std::shared_ptr<Lambdas>>(module, "smoke_Lambdas")
        .def("__gluecodium_id__", [](const Lambdas& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
                .def("deconfuse", [](Lambdas& self, const ::std::string& value, const ::std::function<::std::function<::std::string()>(const ::std::string&)>& confuser) -> py::object {
                        return py::cast(self.deconfuse(value, confuser));
                }, py::arg("value"), py::arg("confuser"))
                .def_static("fuse", [](const ::std::vector< ::std::string >& items, const ::std::function<int32_t(const ::std::string&, const float)>& callback) -> py::object {
                        return gluecodium::python::to_python_regular(Lambdas::fuse(items, callback));
                }, py::arg("items"), py::arg("callback"))
        ;


}
