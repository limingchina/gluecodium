

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
#include "smoke/StructsWithMethodsInterface.h"
#include "smoke/ValidationUtils.h"
#include "string"

using StructsWithMethodsInterface = ::smoke::StructsWithMethodsInterface;
using Vector3 = ::smoke::StructsWithMethodsInterface::Vector3;
using StructWithStaticMethodsOnly = ::smoke::StructsWithMethodsInterface::StructWithStaticMethodsOnly;



void register_smoke_StructsWithMethodsInterface(py::module_& module) {
auto cls_StructsWithMethodsInterface = py::class_<StructsWithMethodsInterface, std::shared_ptr<StructsWithMethodsInterface>>(module, "smoke_StructsWithMethodsInterface")
        .def("__gluecodium_id__", [](const StructsWithMethodsInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_StructsWithMethodsInterfaceVector3 = py::class_<Vector3>(cls_StructsWithMethodsInterface, "Vector3")
        .def_property("x", [](const Vector3& self) -> decltype(auto) {
            return
                (self.x)
            ;
        }, [](Vector3& self, const double value) {

                self.x = value;

        })
        .def_property("y", [](const Vector3& self) -> decltype(auto) {
            return
                (self.y)
            ;
        }, [](Vector3& self, const double value) {

                self.y = value;

        })
        .def_property("z", [](const Vector3& self) -> decltype(auto) {
            return
                (self.z)
            ;
        }, [](Vector3& self, const double value) {

                self.z = value;

        })
        .def(py::init<>())
        .def(py::init<double, double, double>(), py::arg("x"), py::arg("y"), py::arg("z"))
        .def("distance_to", &Vector3::distance_to, py::arg("other"), py::call_guard<py::gil_scoped_release>())
        .def("add", &Vector3::add, py::arg("other"), py::call_guard<py::gil_scoped_release>())
        .def_static("validate", &Vector3::validate, py::arg("x"), py::arg("y"), py::arg("z"), py::call_guard<py::gil_scoped_release>())
        .def_static("create", py::overload_cast<const ::std::string&>(Vector3::create), py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_static("create", py::overload_cast<const ::smoke::StructsWithMethodsInterface::Vector3&>(Vector3::create), py::arg("other"), py::call_guard<py::gil_scoped_release>())
        ;

auto cls_StructsWithMethodsInterfaceStructWithStaticMethodsOnly = py::class_<StructWithStaticMethodsOnly>(cls_StructsWithMethodsInterface, "StructWithStaticMethodsOnly")
        .def(py::init<>())
        .def_static("do_stuff", &StructWithStaticMethodsOnly::do_stuff, py::call_guard<py::gil_scoped_release>())
        ;


}
