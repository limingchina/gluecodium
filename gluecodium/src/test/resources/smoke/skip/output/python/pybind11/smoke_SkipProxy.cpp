

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipProxy.h"
#include "smoke/SkippedEverywhere.h"
#include "smoke/SkippedEverywhereEnum.h"
#include "string"

void register_SkipProxy(py::module_& module) {
    py::class_<SkipProxy, std::shared_ptr<SkipProxy>>(module, "SkipProxy")
        .def("not_in_java", &SkipProxy::not_in_java, py::arg("input"))
        .def("not_in_swift", &SkipProxy::not_in_swift, py::arg("input"))
        .def("not_in_dart", &SkipProxy::not_in_dart, py::arg("input"))
        .def("not_in_kotlin", &SkipProxy::not_in_kotlin, py::arg("input"))
        .def_property("skipped_in_java", &SkipProxy::get_skipped_in_java)
        .def_property("is_skipped_in_swift", &SkipProxy::is_skipped_in_swift)
        .def_property("skipped_in_dart", &SkipProxy::get_skipped_in_dart)
        .def_property("skipped_in_kotlin", &SkipProxy::get_skipped_in_kotlin)
        .def_property("skipped_everywhere", &SkipProxy::get_skipped_everywhere)
        .def_property("skipped_everywhere_too", &SkipProxy::get_skipped_everywhere_too)
        ;
}

